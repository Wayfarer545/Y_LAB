from antagonistfinder import AntagonistFinder
from weapons import Shotgun, Kick


class SuperHero:
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)


class Superman(Kick, SuperHero):
    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)


class Norris(Shotgun, SuperHero):
    def __init__(self):
        super(Norris, self).__init__('Chack Norris', False)
