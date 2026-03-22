# для Google Colab: вставьте код в ячейку и запустите


class Animal:
    """базовый класс для всех животных"""

    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return '...'

    def __str__(self):
        return f'{self.__class__.__name__}({self.name})'


class Dog(Animal):
    def make_sound(self):
        return 'Гав!'


class Cat(Animal):
    def make_sound(self):
        return 'Мяу!'


class Bird(Animal):
    def make_sound(self):
        return 'Чирик!'


# фабрика создаёт нужный класс по строке-типу
def create_animal(animal_type, name):
    types = {
        'dog': Dog,
        'cat': Cat,
        'bird': Bird,
    }
    cls = types.get(animal_type.lower())
    if cls is None:
        raise ValueError(f'неизвестный тип животного: {animal_type}')
    return cls(name)


def make_all_sounds(animals):
    """вызывает make_sound у каждого животного — полиморфизм"""
    for animal in animals:
        print(f'{animal}: {animal.make_sound()}')


# создаём разных животных через фабрику
zoo = [
    create_animal('dog', 'Бобик'),
    create_animal('cat', 'Мурка'),
    create_animal('bird', 'Кеша'),
    Dog('Рекс'),
    Cat('Пушок'),
    Bird('Попугай'),
]

print('звуки животных в зоопарке:')
make_all_sounds(zoo)

print('\nтип каждого животного:')
for animal in zoo:
    print(f'  {animal.name} — {type(animal).__name__}')

# попытка создать неизвестный тип
try:
    create_animal('fish', 'Немо')
except ValueError as e:
    print(f'\nошибка: {e}')
