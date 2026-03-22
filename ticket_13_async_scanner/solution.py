# для Google Colab: !pip install aiohttp nest_asyncio
# затем вставьте код в ячейку и запустите
import asyncio
import time

try:
    import aiohttp
except ImportError:
    print('установите aiohttp: pip install aiohttp')
    raise

# применяем nest_asyncio чтобы работало в Colab/Jupyter
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass

SITES = [
    'https://google.com',
    'https://github.com',
    'https://python.org',
    'https://stackoverflow.com',
    'https://wikipedia.org',
]


async def check_site(session, url, semaphore):
    async with semaphore:
        start = time.time()
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with session.get(url, timeout=timeout) as response:
                elapsed = time.time() - start
                return {'url': url, 'status': response.status, 'time': elapsed}
        except Exception:
            elapsed = time.time() - start
            return {'url': url, 'status': 'ошибка', 'time': elapsed}


async def scan_sites():
    # не более 3 одновременных запросов
    semaphore = asyncio.Semaphore(3)
    async with aiohttp.ClientSession() as session:
        tasks = [check_site(session, url, semaphore) for url in SITES]
        results = await asyncio.gather(*tasks)

    # вывод в табличном виде
    print(f"{'сайт':<40} {'статус':<10} {'время'}")
    print('-' * 65)
    for r in results:
        print(f"{r['url']:<40} {str(r['status']):<10} {r['time']:.2f} сек")


asyncio.run(scan_sites())
