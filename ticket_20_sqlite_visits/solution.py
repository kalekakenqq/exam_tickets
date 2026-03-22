# для Google Colab: вставьте код в ячейку и запустите
import sqlite3
import random
import time

DB = 'visits.db'


def setup():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            page       TEXT NOT NULL,
            visit_time TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def add_test_data(conn, count=1000):
    pages = ['/home', '/about', '/shop', '/contact', '/blog', '/news']
    data = [
        (random.randint(1, 100), random.choice(pages), f'2024-{random.randint(1,12):02d}-{random.randint(1,28):02d}')
        for _ in range(count)
    ]
    conn.executemany('INSERT INTO visits (user_id, page, visit_time) VALUES (?, ?, ?)', data)
    conn.commit()
    print(f'добавлено {count} записей')


def measure_query(conn, user_id):
    start = time.perf_counter()
    result = conn.execute(
        'SELECT COUNT(*) FROM visits WHERE user_id = ?',
        (user_id,)
    ).fetchone()[0]
    elapsed = time.perf_counter() - start
    return elapsed, result


conn = setup()
add_test_data(conn, 1000)

# замеряем без индекса
t1, count = measure_query(conn, 10)
print(f'\nбез индекса: {t1 * 1000:.4f} мс (найдено {count} записей)')

# создаём индекс по user_id
conn.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON visits(user_id)')
conn.commit()

# замеряем с индексом
t2, count = measure_query(conn, 10)
print(f'с индексом:  {t2 * 1000:.4f} мс (найдено {count} записей)')

# при малом объёме данных разница может быть незаметна
if t1 > 0 and t2 > 0:
    ratio = t1 / t2
    print(f'соотношение времени: {ratio:.1f}x')
print('(на большом объёме данных индекс даёт значительный прирост)')

conn.close()
