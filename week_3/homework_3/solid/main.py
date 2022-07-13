from heroes import Superman, Norris, SuperHero
from places import Kostroma, Tokyo, Place
from media import News


def save_the_place(hero: SuperHero, place: Place):
    """
    Функция точки входа.

    Поиск злодея, атака (стандартная + ульта, если герой умеет),
    Передача информации СМИ для освещения событий.
    """

    hero.find(place)
    hero.attack()
    if hero.can_use_ultimate_attack:
        hero.super_attack(hero.name)
    News(hero.name, place.name).create_tv_news()


if __name__ == '__main__':
    save_the_place(Superman(), Kostroma())
    print('-' * 20)
    save_the_place(Norris(), Tokyo())
    print('-' * 20)