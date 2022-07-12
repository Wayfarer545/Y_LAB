import time
from functools import wraps


def delay_runner(
		call_count: int,
		start_sleep_time: float,
		factor: float,
		border_sleep_time: float
		):
	def func_interceptor(func):
		@wraps(func)
		def wrapper(**kwargs):
			print('Начало работы')
			t = start_sleep_time
			iter_count: int = 1
			while iter_count <= call_count:
				result = func()
				print(f'Запуск номер {iter_count}. Ожидание: {t} секунд. '
				      f'Результат декорируемой функции = {result}.')
				iter_count += 1
				time.sleep(t)
				t *= factor
				if t > border_sleep_time:
					t = border_sleep_time
			print('Конец работы')
		return wrapper
	return func_interceptor

@delay_runner(call_count=5, start_sleep_time=1, factor=2, border_sleep_time=17)
def sample_func():
	return 666


if __name__ == '__main__':
	sample_func()