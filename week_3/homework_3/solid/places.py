from abc import ABC, abstractmethod


class Place(ABC):
    """
    Модель класса для создания городов.

    Присутствует обязательный метод поиска противника.
    """
    name: str

    @abstractmethod
    def get_enemy(self):
        print('Bitcoin costs lower than 100$ or something')


class Kostroma(Place):
    name: str = 'Kostroma'

    def get_enemy(self):
        print('Orcs hid in the forest')


class Tokyo(Place):
    name: str = 'Tokyo'

    def get_enemy(self):
        print('Godzilla stands near a skyscraper')
