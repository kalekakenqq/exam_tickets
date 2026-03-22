# для Google Colab: вставьте код в ячейку и запустите
# изображения скачиваются с picsum.photos (нужен интернет)
import urllib.request
import threading
import time
import os

# список публичных тестовых изображений
IMAGE_URLS = [
    'https://picsum.photos/seed/1/400/300',
    'https://picsum.photos/seed/2/400/300',
    'https://picsum.photos/seed/3/400/300',
    'https://picsum.photos/seed/4/400/300',
    'https://picsum.photos/seed/5/400/300',
]

os.makedirs('downloads', exist_ok=True)


def download_image(url, index):
    filename = f'downloads/image_{index + 1}.jpg'
    urllib.request.urlretrieve(url, filename)
    print(f'скачано: image_{index + 1}.jpg')


def sequential_download():
    """загрузка по одному"""
    print('последовательная загрузка...')
    start = time.time()
    for i, url in enumerate(IMAGE_URLS):
        download_image(url, i)
    elapsed = time.time() - start
    print(f'время: {elapsed:.2f} сек')
    return elapsed


def parallel_download():
    """загрузка всех одновременно в отдельных потоках"""
    print('параллельная загрузка...')
    start = time.time()
    threads = []
    for i, url in enumerate(IMAGE_URLS):
        t = threading.Thread(target=download_image, args=(url, i))
        threads.append(t)
        t.start()
    # ждём завершения всех потоков
    for t in threads:
        t.join()
    elapsed = time.time() - start
    print(f'время: {elapsed:.2f} сек')
    return elapsed


seq_time = sequential_download()
par_time = parallel_download()

print(f'\nпоследовательно: {seq_time:.2f} сек')
print(f'параллельно:    {par_time:.2f} сек')
if par_time > 0:
    print(f'ускорение: {seq_time / par_time:.1f}x')
print('изображения сохранены в папку downloads/')
