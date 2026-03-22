# для Google Colab: !pip install nest_asyncio
# в Colab таймер работает без интерактивной паузы
import asyncio
import threading
import sys

# применяем nest_asyncio чтобы работало в Colab/Jupyter
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

paused = False
running = True


def input_listener():
    """читает команды из терминала в отдельном потоке"""
    global paused, running
    while running:
        try:
            cmd = input()
            if cmd.strip() == 'p':
                paused = not paused
                print('[пауза]' if paused else '[продолжение]', flush=True)
            elif cmd.strip() == 'q':
                running = False
        except EOFError:
            break


async def countdown(seconds):
    global paused, running
    remaining = seconds

    print(f'таймер запущен на {seconds} сек')
    # команды работают только в терминале
    if sys.stdin.isatty():
        print('команды: p — пауза/продолжение, q — выход')

    while remaining > 0 and running:
        if not paused:
            print(f'осталось: {remaining} сек', flush=True)
            remaining -= 1
        await asyncio.sleep(1)

    running = False
    if remaining == 0:
        print('время вышло!')
    else:
        print('остановлено')


async def main():
    global running
    try:
        seconds = int(input('введите время в секундах: '))
    except (ValueError, EOFError):
        seconds = 5
        print(f'используем {seconds} секунд')

    # запускаем поток для чтения команд только в терминале
    if sys.stdin.isatty():
        t = threading.Thread(target=input_listener, daemon=True)
        t.start()

    await countdown(seconds)


asyncio.run(main())
