# для Google Colab: вставьте код в ячейку — запустится демо
# для терминала: python solution.py
import sqlite3
import hashlib
import sys

DB = 'users.db'


def get_conn():
    return sqlite3.connect(DB)


def setup():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            username      TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register(username, password):
    conn = get_conn()
    try:
        # параметризованный запрос защищает от sql-инъекции
        conn.execute(
            'INSERT INTO users (username, password_hash) VALUES (?, ?)',
            (username, hash_password(password))
        )
        conn.commit()
        print(f'пользователь {username} зарегистрирован')
        return True
    except sqlite3.IntegrityError:
        print(f'пользователь {username} уже существует')
        return False
    finally:
        conn.close()


def login(username, password):
    conn = get_conn()
    # параметризованный запрос — безопасный вариант
    cur = conn.execute(
        'SELECT password_hash FROM users WHERE username = ?',
        (username,)
    )
    row = cur.fetchone()
    conn.close()
    if row and row[0] == hash_password(password):
        print(f'вход выполнен: {username}')
        return True
    print('неверный логин или пароль')
    return False


def interactive():
    """консольный интерфейс для терминала"""
    setup()
    while True:
        print('\n1. регистрация  2. вход  3. выход')
        choice = input('выберите: ').strip()
        if choice == '1':
            u = input('логин: ')
            p = input('пароль: ')
            register(u, p)
        elif choice == '2':
            u = input('логин: ')
            p = input('пароль: ')
            login(u, p)
        elif choice == '3':
            break


def demo():
    """демонстрация для Google Colab"""
    setup()
    print('--- демонстрация системы авторизации ---')
    register('alice', 'password123')
    register('bob', 'secret456')
    register('alice', 'other')  # попытка зарегистрировать повторно
    print()
    login('alice', 'password123')  # верный пароль
    login('alice', 'wrongpass')    # неверный пароль
    login('unknown', '123')        # несуществующий пользователь


# в colab stdin не tty — запускаем демо
if sys.stdin.isatty():
    interactive()
else:
    demo()
