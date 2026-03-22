# для Google Colab: вставьте код в ячейку и запустите
import threading
import queue
import random
import time

# очередь с максимальным размером 10
Q = queue.Queue(maxsize=10)

# время работы системы в секундах
RUNTIME = 5
stop_event = threading.Event()


def producer(name):
    """генерирует случайные числа и кладёт в очередь"""
    while not stop_event.is_set():
        num = random.randint(1, 100)
        try:
            Q.put(num, timeout=0.5)
            print(f'производитель {name}: добавил {num}')
        except queue.Full:
            pass
        time.sleep(random.uniform(0.2, 0.5))


def consumer(name):
    """берёт числа из очереди и вычисляет квадрат"""
    while not stop_event.is_set() or not Q.empty():
        try:
            item = Q.get(timeout=0.5)
            result = item ** 2
            print(f'потребитель {name}: {item}^2 = {result}')
            Q.task_done()
        except queue.Empty:
            if stop_event.is_set():
                break


# запускаем 2 производителей и 3 потребителей
producers = [threading.Thread(target=producer, args=(f'П{i + 1}',)) for i in range(2)]
consumers = [threading.Thread(target=consumer, args=(f'П{i + 1}',)) for i in range(3)]

for c in consumers:
    c.start()
for p in producers:
    p.start()

# останавливаем по истечении времени
time.sleep(RUNTIME)
stop_event.set()

for p in producers:
    p.join()
for c in consumers:
    c.join()

print('\nвсе задачи выполнены')
