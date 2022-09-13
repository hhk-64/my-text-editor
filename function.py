from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os


class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.setMinimumSize(720, 480)
		self.setWindowTitle("Text Editor")
		self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_FileIcon")))

		self.layout = QHBoxLayout()


		self.menuBar = QMenuBar(self)
		self.FileMenu = self.menuBar.addMenu("File")
		self.FileMenu.NewFileAction = self.FileMenu.addAction("New File...")
		self.FileMenu.OpenFileAction = self.FileMenu.addAction("Open File...")
		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())


		self.TextArea = QPlainTextEdit(self)
		self.TextArea.move(QPoint(0, 0+self.menuBar.height()))
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height())


		self.FileMenu.NewFileAction.triggered.connect(self.CreateFile)
	


	def resizeEvent(self, event):
		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height())
		return super(MainWindow, self).resizeEvent(event)
	

	@Slot()
	def CreateFile(self):
		f = QFileDialog.getSaveFileName(self, "Create a new file")[0]
		with open(f, "w", encoding="UTF-8") as f:
			pass