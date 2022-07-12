class Attack:
	def __init__(self, name):
		self.name = name

	@staticmethod
	def fire_a_gun():
		print('PIU PIU')

	@staticmethod
	def roundhouse_kick():
		print('Bump')

	def ultimate(self, name):
		if name == 'Clark Kent':
			print('Wzzzuuuup!')