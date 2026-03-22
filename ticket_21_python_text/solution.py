# для Google Colab: вставьте код в ячейку и запустите
import re
from collections import Counter

# стоп-слова — предлоги, союзы, частицы
STOP_WORDS = {
    'и', 'в', 'не', 'на', 'с', 'а', 'но', 'или', 'по', 'из', 'за',
    'от', 'к', 'о', 'у', 'до', 'как', 'что', 'это', 'для', 'при',
    'же', 'бы', 'то', 'ни', 'уже', 'ещё', 'тот', 'так', 'все', 'об',
}

SAMPLE_TEXT = """
Python это мощный язык программирования. Python используется в веб-разработке
и в науке о данных. Язык Python прост и удобен для изучения программирования.
Многие разработчики выбирают Python за простоту и мощность. Веб-разработка
на Python позволяет создавать быстрые и надёжные приложения. Python хорош
для начинающих и опытных разработчиков. Язык программирования Python
поддерживает множество парадигм. Разработчики любят Python за читаемость кода.
Библиотеки Python помогают решать сложные задачи. Сообщество Python огромно.
"""


def analyze_text(text):
    # разбиваем на слова, убираем знаки препинания
    words = re.findall(r'[а-яёa-z]+', text.lower())
    # удаляем стоп-слова
    words = [w for w in words if w not in STOP_WORDS]

    freq = Counter(words)
    top10 = freq.most_common(10)

    return top10


# создаём файл с текстом
with open('sample.txt', 'w', encoding='utf-8') as f:
    f.write(SAMPLE_TEXT)

# читаем и анализируем
with open('sample.txt', 'r', encoding='utf-8') as f:
    text = f.read()

top10 = analyze_text(text)

print('топ-10 самых частых слов:')
for i, (word, count) in enumerate(top10, 1):
    print(f'  {i:2}. {word}: {count}')

# сохраняем результат
with open('result.txt', 'w', encoding='utf-8') as f:
    f.write('топ-10 слов:\n')
    for word, count in top10:
        f.write(f'{word}: {count}\n')

print('\nрезультат сохранён в result.txt')
