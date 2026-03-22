# для Google Colab: вставьте код в ячейку и запустите
import threading
import time


def run_demo(use_lock):
    account = {'balance': 1000}
    lock = threading.Lock()

    def withdraw(amount, name):
        if use_lock:
            lock.acquire()

        # читаем текущий баланс
        current = account['balance']
        # небольшая задержка делает race condition заметной
        time.sleep(0.01)

        if current >= amount:
            account['balance'] = current - amount
            print(f'{name}: снял {amount}, остаток {account["balance"]}')
        else:
            print(f'{name}: недостаточно средств (баланс {account["balance"]})')

        if use_lock:
            lock.release()

    threads = [
        threading.Thread(target=withdraw, args=(250, f'поток-{i + 1}'))
        for i in range(5)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return account['balance']


print('=== без синхронизации (может дать неверный результат) ===')
final = run_demo(use_lock=False)
print(f'итоговый баланс: {final} (ожидалось 250 или 0)\n')

print('=== с блокировкой Lock (всегда корректный результат) ===')
final = run_demo(use_lock=True)
print(f'итоговый баланс: {final} (корректно)')
