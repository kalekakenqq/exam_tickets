# для Google Colab: вставьте код в ячейку и запустите
import time
import functools


def timer(func):
    """измеряет время выполнения функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f'{func.__name__} выполнилась за {elapsed:.4f} сек')
        return result
    return wrapper


def retry(max_attempts=3):
    """повторяет выполнение при исключении"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'попытка {attempt}/{max_attempts} не удалась: {e}')
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator


def cache(func):
    """кэширует результаты вызовов функции"""
    cached = {}

    @functools.wraps(func)
    def wrapper(*args):
        if args in cached:
            print(f'  [кэш] для {args}')
            return cached[args]
        result = func(*args)
        cached[args] = result
        return result

    return wrapper


# применяем все декораторы к тяжёлой функции
@timer
@cache
def heavy_calculation(n):
    """имитирует долгое вычисление"""
    time.sleep(0.1)
    return sum(range(n))


@retry(max_attempts=3)
def unreliable_function():
    """иногда падает с ошибкой"""
    import random
    if random.random() < 0.6:
        raise ValueError('временная ошибка')
    return 'успех!'


print('--- тест @timer и @cache ---')
r1 = heavy_calculation(1000000)
r2 = heavy_calculation(1000000)  # берётся из кэша
r3 = heavy_calculation(2000000)  # новое вычисление
print()

print('--- тест @retry ---')
try:
    result = unreliable_function()
    print(f'результат: {result}')
except ValueError:
    print('все попытки исчерпаны')
