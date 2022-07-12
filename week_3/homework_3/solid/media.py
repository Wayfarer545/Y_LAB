from typing import Optional
from heroes import SuperHero
from places import Place


class News:
	def __init__(self, hero: str, place: str):
		self.name = hero
		self.place_name = place

	def create_tv_news(self):
		print(f'    BREAKING NEWS!!!\n    '
		      f'Melanie Collins says: \n    '
		      f'omg! {self.name} just saved the {self.place_name}!')