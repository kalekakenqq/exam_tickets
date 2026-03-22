# для Google Colab: вставьте код в ячейку и запустите
import sqlite3

DB = 'library.db'


def setup():
    conn = sqlite3.connect(DB)
    conn.execute('PRAGMA foreign_keys = ON')  # включаем поддержку внешних ключей
    conn.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT NOT NULL,
            author_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
    """)
    # добавляем тестовые данные
    conn.executemany('INSERT OR IGNORE INTO authors VALUES (?, ?)', [
        (1, 'Лев Толстой'),
        (2, 'Фёдор Достоевский'),
        (3, 'Антон Чехов'),
        (4, 'Александр Пушкин'),  # без книг — для демонстрации
    ])
    conn.executemany('INSERT OR IGNORE INTO books VALUES (?, ?, ?)', [
        (1, 'Война и мир',                  1),
        (2, 'Анна Каренина',                1),
        (3, 'Преступление и наказание',      2),
        (4, 'Идиот',                         2),
        (5, 'Вишнёвый сад',                  3),
    ])
    conn.commit()
    return conn


def all_books_with_authors(conn):
    rows = conn.execute("""
        SELECT books.title, authors.name
        FROM books
        JOIN authors ON books.author_id = authors.id
        ORDER BY authors.name
    """).fetchall()
    print('все книги с авторами:')
    for title, author in rows:
        print(f'  "{title}" — {author}')


def books_by_author(conn, author_name):
    rows = conn.execute("""
        SELECT books.title
        FROM books
        JOIN authors ON books.author_id = authors.id
        WHERE authors.name = ?
    """, (author_name,)).fetchall()
    print(f'\nкниги автора {author_name}:')
    for row in rows:
        print(f'  "{row[0]}"')


def authors_without_books(conn):
    rows = conn.execute("""
        SELECT authors.name
        FROM authors
        LEFT JOIN books ON authors.id = books.author_id
        WHERE books.id IS NULL
    """).fetchall()
    print('\nавторы без книг:')
    if rows:
        for row in rows:
            print(f'  {row[0]}')
    else:
        print('  нет')


conn = setup()
all_books_with_authors(conn)
books_by_author(conn, 'Лев Толстой')
authors_without_books(conn)
conn.close()
