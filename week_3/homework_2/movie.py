from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import Generator, List, Tuple


@dataclass
class Movie:
	title: str
	dates: List[Tuple[datetime, datetime]]

	def schedule(self) -> Generator[datetime, None, None]:
		for period in self.dates:
			premier_day, closing_day = period
			delta = closing_day - premier_day
			for i in range(delta.days + 1):
				show_day = premier_day + timedelta(i)
				yield show_day


if __name__ == "__main__":
	m = Movie('sw', [
		(datetime(2020, 1, 1), datetime(2020, 1, 7)),
		(datetime(2020, 1, 15), datetime(2020, 2, 7))
	])

	for d in m.schedule():
		print(d)

