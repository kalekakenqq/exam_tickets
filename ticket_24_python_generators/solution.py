# для Google Colab: вставьте код в ячейку и запустите
import os


def fibonacci():
    """бесконечная последовательность чисел фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_lines(filepath):
    """читает файл построчно без загрузки в память"""
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            yield line.rstrip()


def infinite_counter(start=0, step=1):
    """бесконечная арифметическая последовательность"""
    n = start
    while True:
        yield n
        n += step


# демонстрация 1 — числа фибоначчи
print('первые 10 чисел фибоначчи:')
fib = fibonacci()
print([next(fib) for _ in range(10)])

# использование в цикле for
print('\nчисла фибоначчи до 200:')
for n in fibonacci():
    if n > 200:
        break
    print(n, end=' ')
print()

# демонстрация 2 — чтение файла построчно
with open('lines.txt', 'w', encoding='utf-8') as f:
    f.write('первая строка\nвторая строка\nтретья строка')

print('\nстроки из файла:')
for line in read_lines('lines.txt'):
    print(f'  {line}')
os.remove('lines.txt')

# демонстрация 3 — бесконечный счётчик с next()
print('\nпервые 5 чётных чисел (шаг 2):')
counter = infinite_counter(0, 2)
for _ in range(5):
    print(next(counter), end=' ')
print()
