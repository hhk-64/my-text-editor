from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os, json

from shiboken6 import isValid


class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.setMinimumSize(720, 480)
		self.setWindowTitle("Text Editor")
		self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_FileIcon")))

		self.layout = QHBoxLayout()


		if not ReadJsonFile(): self.settingsData = CreateJsonFile()
		else: self.settingsData = ReadJsonFile()

		self.font_ = QFont()
		self.font_.fromString(self.settingsData[0]["font"])

		self.color_ = self.settingsData[0]["color"]


		self.textBuffer = ["", False]
		self.curFile = ""


		self.menuBar = QMenuBar(self)

		self.FileMenu = self.menuBar.addMenu("File")

		self.FileMenu.NewFileAction = self.FileMenu.addAction("New File...")
		self.FileMenu.NewFileAction.triggered.connect(self.CreateFile)

		self.FileMenu.OpenFileAction = self.FileMenu.addAction("Open File...")
		self.FileMenu.OpenFileAction.triggered.connect(self.OpenFile)

		self.FileMenu.addSeparator()

		self.FileMenu.SaveAction = self.FileMenu.addAction("Save")
		self.FileMenu.SaveAction.triggered.connect(self.SaveFile)
		self.FileMenu.SaveAction.setDisabled(True)

		self.FileMenu.SaveAsAction = self.FileMenu.addAction("Save As...")
		self.FileMenu.SaveAsAction.triggered.connect(self.SaveFileAs)

		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())


		self.menuBar.SettingsMenu = self.menuBar.addMenu("Settings")
		
		self.menuBar.SettingsMenu.ChangeFontAction = self.menuBar.SettingsMenu.addAction("Change Font...")
		self.menuBar.SettingsMenu.ChangeFontAction.triggered.connect(self.changeFont)

		self.menuBar.SettingsMenu.ChangeColorAction = self.menuBar.SettingsMenu.addAction("Change Color...")
		self.menuBar.SettingsMenu.ChangeColorAction.triggered.connect(self.changeColor)
		
		self.curFileDisplay = QLabel("No File opened", self)
		self.curFileDisplay.setStyleSheet("padding-left: 2px")
		self.curFileDisplay.setFixedSize(self.width(), 25)
		self.curFileDisplay.move(0, self.height()-self.curFileDisplay.sizeHint().height())


		self.TextArea = QTextEdit(self)
		self.TextArea.move(QPoint(0, 0+self.menuBar.height()))
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height()-self.curFileDisplay.height())
		self.TextArea.setFont(self.font_)
		self.TextArea.setStyleSheet(f"color: {self.color_}")
		self.TextArea.textChanged.connect(self.CheckSaveBuffer)
	


	def resizeEvent(self, event):
		self.menuBar.setFixedSize(self.width(), self.menuBar.sizeHint().height())
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height()-self.curFileDisplay.height())
		self.curFileDisplay.setFixedSize(self.width(), 25)
		self.curFileDisplay.move(0, self.height()-self.curFileDisplay.sizeHint().height())
		return super(MainWindow, self).resizeEvent(event)
	

	
	@Slot()
	def CreateFile(self):
		f = QFileDialog.getSaveFileName(self, "Create a new file", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f == "": return
		
		with open(f, "w", encoding="UTF-8") as fl:
			self.textBuffer = ["", True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
	
	@Slot()
	def OpenFile(self):
		f = QFileDialog.getOpenFileName(self, "Open a file", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f != "":
			with open(f, "r", encoding="UTF-8") as fl:
				content = fl.read()
				self.TextArea.setPlainText(content)
				self.textBuffer = [content, True]
				self.curFile = f
				self.curFileDisplay.setText(self.curFile)
	
	@Slot()
	def CheckSaveBuffer(self):
		if self.textBuffer[1] == False: return
		
		if self.TextArea.toPlainText() != self.textBuffer[0]: self.FileMenu.SaveAction.setDisabled(False)
		elif self.TextArea.toPlainText() == self.textBuffer[0]: self.FileMenu.SaveAction.setDisabled(True)
	
	@Slot()
	def SaveFile(self):
		if self.curFile == "": return

		with open(self.curFile, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer[0] = content
			self.FileMenu.SaveAction.setDisabled(True)
	
	@Slot()
	def SaveFileAs(self):
		f = QFileDialog.getSaveFileName(self, "Save File As", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f == "": return
		
		with open(f, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer = [content, True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
	
	@Slot()
	def changeFont(self):
		font = QFontDialog.getFont(self)
		if font[0] == False: return
		self.TextArea.setFont(font[1])
		data = ["font", font]
		UpdateJsonFile(self.settingsData[1], data)
	
	@Slot()
	def changeColor(self):
		color = QColorDialog(self).getColor()
		if color.isValid() == False: return
		cursor = self.TextArea.textCursor()
		initPos = cursor.position()
		cursor.movePosition(cursor.Start, cursor.MoveAnchor)
		cursor.movePosition(cursor.End, cursor.KeepAnchor)
		fg = QTextCharFormat()
		fg.setForeground(QBrush(color))
		cursor.setCharFormat(fg)
		cursor.clearSelection()
		self.color_ = color.name()
		self.TextArea.setStyleSheet(f"color: {self.color_}")
		cursor.setPosition(initPos)
		data = ["color", color.name()]
		UpdateJsonFile(self.settingsData[1], data)
	




def ReadJsonFile():
	try:
		with open("settings.json", "r") as f:
			data = json.load(f)
			if "font" not in data.keys() or "color" not in data.keys(): return False
			else: return [data, os.path.realpath(f.name)]
	except:
		return False

def CreateJsonFile():
	with open("settings.json", "w") as f:
		data = {
			"font": "Arial,16,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Standard",
			"color": "#000000"
		}
		json.dump(data, f, indent=4)
		return [data, os.path.realpath(f.name)]

def UpdateJsonFile(f, ctx):
	if ctx[0] == "font":
		with open(f, "r") as fl:
			try:
				data = json.load(fl)
			except:
				CreateJsonFile()
				return
		
		data["font"] = ctx[1].toString()

		with open(f, "w") as fl:
			json.dump(data, fl, indent=4)


	if ctx[0] == "color":
		with open(f, "r") as fl:
			try:
				data = json.load(fl)
			except:
				CreateJsonFile()
				return
		
		data["color"] = ctx[1]

		with open(f, "w") as fl:
			json.dump(data, fl, indent=4)