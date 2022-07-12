from typing import Iterable, Generator, Optional

class CyclicIterator:
	def __init__(self, objects: Iterable):
		self.objects = None
		try:
			iter(objects)
			self.objects = objects
			self.sample_generator = self.__iter__()
		except TypeError:
			raise exit('Входные данные не инерируемы!')

	def __iter__(self):
		while True:
			for i in self.objects:
				yield i

	def __next__(self):
		return next(self.sample_generator)


if __name__ == "__main__":
	cyclic_iterator = CyclicIterator(range(3))
	for i in cyclic_iterator:
		print(i)