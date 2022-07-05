import random
import time
import tkinter as tk
from tkinter import Tk, messagebox, Button
import numpy as np


class App(Tk):
	# инициализация игрового поля и переменных
	def __init__(self):
		super().__init__()
		self.resizable(0, 0)
		self.title("Reversed XO")
		self["bg"] = "#badee2"
		self.matrix = np.zeros((10, 10))
		self.buttons = self.init_buttons()
		self.empty_cells = list(np.arange(0, 100))

	# первичная инициализация кнопок поля
	def init_buttons(self) -> list[tk.Button]:
		buttons = []
		for i in range(10):
			self.grid_columnconfigure(i, minsize=50)
			for j in range(10):
				button = Button(
					self.master,
					text='',
					font=('TkHeadingFont', 20),
					bg='#28393a',
					fg='#02fa2c',
					cursor='hand2',
					activebackground='#28393a',
					activeforeground='#16e512',
					highlightcolor='#36ffd0',
					state='normal',
					command=lambda x=i, y=j: self.on_click(f'{x}{y}')
				)
				button.grid(row=i, column=j, stick="wens")
				buttons.append(button)
		return buttons

	# логика по юзерскому клику в ячейку поля
	def on_click(self, x):
		btn = self.buttons[int(x)]
		if btn['text'] == "":
			btn['text'] = 'X'
			self.matrix_update(self.matrix, btn, 1)
			if self.fail_check(self.matrix)[0]:
				return self.mbox(mode=1)
			elif self.ai_turn():
				return self.mbox(mode=2)

	# рандом функция ответного хода
	def ai_turn(self):
		while len(self.empty_cells) > 0:
			target = random.choice(self.empty_cells)
			matrix = np.copy(self.matrix)
			self.matrix_update(matrix, self.buttons[target], 2)
			if self.fail_check(matrix) != (True, 2) and self.buttons[target]['text'] == '':
				self.buttons[target]['text'] = 'O'
				self.buttons[target]['fg'] = '#f33'
				self.matrix_update(self.matrix, self.buttons[target], 2)
				return False
			else:
				self.empty_cells.remove(target)
				continue
		return True

	# проверка поля на наличие проигрышных комбинаций
	@staticmethod
	def fail_check(matrix) -> (bool, int):
		def vector_processor(vector):
			nonlocal flag, looser
			for k in range(len(vector) - 4):
				count = len(set(vector[k: k + 5]))
				sample = int(vector[k])
				if count == 1 and sample > 0:
					flag = True
					looser = int(vector[k])
					return
				else:
					k += 1

		def mat_processor(matrix):
			for vector in matrix:
				vector_processor(vector)
			for i in range(6):
				vector = np.diagonal(matrix, offset=i, axis1=0, axis2=1)
				vector_processor(vector)
			for i in range(1, 6):
				vector = np.diagonal(matrix, offset=i, axis1=1, axis2=0)
				vector_processor(vector)

		flag = False
		looser = 0
		mat_processor(matrix)
		matrix = np.array(np.rot90(matrix))
		mat_processor(matrix)
		return flag, looser

	# обновление информации в матрице поля
	@staticmethod
	def matrix_update(matrix, btn: tk.Button, mark: int):
		try:
			cell_num = int((str(btn))[8:])
		except:
			cell_num = 1
		finally:
			cell_num -= 1
		matrix[cell_num // 10, cell_num % 10] = mark

	# установка значений в исходное положение после игры
	def reset(self):
		for button in self.buttons:
			button['text'] = ''
			button['fg'] = '#02fa2c'
			button['state'] = 'normal'
		self.matrix = np.zeros((10, 10))
		self.empty_cells = list(np.arange(0, 100))

	# вывод попап сообщения по окончании игры
	def mbox(self, mode=0) -> bool:
		messages = [
			'Reserved',
			'Вы проиграли. Хотите попробовать ещё?',
			'Искусственный интеллект в шоке. Повторим?'
		]
		if messagebox.askyesno('Game over', messages[mode]):
			self.reset()
		else:
			self.quit()


if __name__ == "__main__":
	app = App()
	app.mainloop()