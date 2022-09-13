from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, Slot


class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.setFixedSize(720, 480)
		self.setWindowTitle("Text Editor")