# для Google Colab: вставьте код в ячейку и запустите
import sqlite3

DB = 'students.db'


def create_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name  TEXT NOT NULL,
            age   INTEGER,
            grade INTEGER
        )
    """)
    conn.execute('DELETE FROM students')
    conn.commit()
    return conn


def add_students(conn):
    students = [
        ('Иван Иванов', 20, 5),
        ('Мария Петрова', 19, 4),
        ('Алексей Сидоров', 21, 3),
        ('Елена Козлова', 20, 5),
        ('Дмитрий Новиков', 22, 4),
    ]
    # используем executemany для добавления нескольких записей
    conn.executemany('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', students)
    conn.commit()
    print(f'добавлено {len(students)} студентов')


def show_all(conn):
    rows = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    print('\nвсе студенты:')
    print(f'  {"id":<4} {"имя":<20} {"возраст":<10} {"оценка"}')
    print('  ' + '-' * 42)
    for row in rows:
        print(f'  {row[0]:<4} {row[1]:<20} {row[2]:<10} {row[3]}')


def find_by_grade(conn, grade):
    rows = conn.execute('SELECT * FROM students WHERE grade = ?', (grade,)).fetchall()
    print(f'\nстуденты с оценкой {grade}:')
    for row in rows:
        print(f'  {row[1]} (возраст {row[2]})')


conn = create_db()
add_students(conn)
show_all(conn)
find_by_grade(conn, 5)
conn.close()
print(f'\nданные сохранены в {DB}')
