# для Google Colab: вставьте код в ячейку и запустите
import sqlite3

DB = 'bank.db'


def setup():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id      INTEGER PRIMARY KEY,
            owner   TEXT NOT NULL,
            balance REAL NOT NULL
        )
    """)
    # начальные счета
    conn.executemany('INSERT OR IGNORE INTO accounts VALUES (?, ?, ?)', [
        (1, 'Алиса', 1000.0),
        (2, 'Боб',   500.0),
        (3, 'Карл',  200.0),
    ])
    conn.commit()
    conn.close()


def show_accounts():
    conn = sqlite3.connect(DB)
    rows = conn.execute('SELECT * FROM accounts').fetchall()
    conn.close()
    print('  счета:')
    for row in rows:
        print(f'  [{row[0]}] {row[1]}: {row[2]:.2f} руб.')


def transfer(from_id, to_id, amount):
    conn = sqlite3.connect(DB)
    try:
        # начало транзакции — все операции выполняются или не выполняются
        cur = conn.execute('SELECT balance FROM accounts WHERE id = ?', (from_id,))
        row = cur.fetchone()
        if not row:
            print('счёт отправителя не найден')
            return
        if row[0] < amount:
            print(f'недостаточно средств: баланс {row[0]:.2f}, нужно {amount:.2f}')
            return

        conn.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, from_id))
        conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', (amount, to_id))
        conn.commit()  # фиксируем транзакцию
        print(f'перевод {amount:.2f} руб. выполнен')
    except Exception as e:
        conn.rollback()  # откатываем при ошибке
        print(f'ошибка транзакции: {e}')
    finally:
        conn.close()


setup()
print('начальное состояние:')
show_accounts()

print('\nперевод 300 руб. от Алисы к Бобу:')
transfer(1, 2, 300)
show_accounts()

print('\nпопытка перевести больше баланса (Карл -> Алиса, 500 руб.):')
transfer(3, 1, 500)
show_accounts()
