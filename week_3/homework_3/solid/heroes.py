from antagonistfinder import AntagonistFinder
from weapons import Attack


class SuperHero:
    def __init__(self, name, can_use_ultimate_attack=True):
        self.name = name
        self.can_use_ultimate_attack = can_use_ultimate_attack
        self.finder = AntagonistFinder()

    def find(self, place):
        self.finder.get_antagonist(place)

    def ultimate(self):
        Attack.ultimate(self, self.name)



class Superman(SuperHero):
    def __init__(self):
        super(Superman, self).__init__('Clark Kent', True)

    def attack(self):
        Attack.roundhouse_kick()


class Norris(SuperHero):
    def __init__(self):
        super(Norris, self).__init__('Chack Norris', False)

    def attack(self):
        Attack.fire_a_gun()