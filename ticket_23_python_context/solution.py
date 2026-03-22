# для Google Colab: вставьте код в ячейку и запустите
import time
import os
from contextlib import contextmanager


class Timer:
    """контекстный менеджер для измерения времени блока кода"""

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.time() - self.start
        print(f'время выполнения: {self.elapsed:.4f} сек')
        return False  # не подавляем исключения


@contextmanager
def change_dir(path):
    """временно меняет текущую директорию"""
    old_dir = os.getcwd()
    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    try:
        yield path
    finally:
        os.chdir(old_dir)  # всегда возвращаемся назад


@contextmanager
def safe_open(filepath, mode='r', encoding='utf-8'):
    """открывает файл и гарантирует закрытие"""
    f = open(filepath, mode, encoding=encoding)
    try:
        yield f
    finally:
        f.close()
        print(f'файл {filepath} закрыт')


# демонстрация 1 — измерение времени
print('--- измерение времени ---')
with Timer() as t:
    time.sleep(0.2)
    result = sum(range(1000000))
print(f'сумма: {result}')

# демонстрация 2 — смена директории
print('\n--- временная смена директории ---')
print(f'до: {os.getcwd()}')
with change_dir('temp_folder') as folder:
    print(f'внутри: {os.getcwd()}')
    open('test_file.txt', 'w').close()  # создаём файл
print(f'после: {os.getcwd()}')

# демонстрация 3 — безопасная работа с файлом
print('\n--- безопасная работа с файлом ---')
with safe_open('temp_folder/test_file.txt', 'w') as f:
    f.write('тестовый текст')

with safe_open('temp_folder/test_file.txt', 'r') as f:
    content = f.read()
    print(f'прочитано: {content}')

# очистка
os.remove('temp_folder/test_file.txt')
os.rmdir('temp_folder')
