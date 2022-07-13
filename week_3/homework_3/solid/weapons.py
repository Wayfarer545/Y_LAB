from abc import ABC, abstractmethod


class Attack(ABC):
	heroes_ultimate = {
		'Clark Kent': 'Wzzzuuuup!',
	}

	@abstractmethod
	def attack(self):
		pass

	def super_attack(self, name: str):
		print(self.heroes_ultimate[name])


class Shotgun(Attack):
	def attack(self):
		print('PIU PIU')


class Kick(Attack):
	def attack(self):
		print('Bump')

