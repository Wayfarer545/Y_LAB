from abc import ABC, abstractmethod, abstractproperty


class Place(ABC):
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
