class News:
	"""
	Оповещение о победе героя через СМИ
	"""
	def __init__(self, hero: str, place: str):
		"""
		Получение материалов с места событий.

		В конструктор обязательно передаётся информация о том,
		кто и где одержал победу.
		"""
		self.name = hero
		self.place_name = place

	def create_tv_news(self):
		"""
		Формирование информационного выпуска.

		* Мелани Коллинз - телеведущая.
		"""
		print(f'    BREAKING NEWS!!!\n    '
		      f'Melanie Collins says: \n    '
		      f'omg! {self.name} just saved the {self.place_name}!')