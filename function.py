#	----- CUSTOM COLORS -----	#
BACKGROUND_COLOR = "#424242"
BORDER_COLOR = "#212121"
PRIMARY_COLOR = "#616161"
SECONDARY_COLOR = "#BDBDBD"
HOVER_COLOR = "#212121"
#	-------------------------	#



from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import os, json, functools





class FunctionButton(QPushButton):

	def __init__(self, parent, txt, endColor):

		super().__init__()
		self.setParent(parent)
		self.setText(txt)

		self._curColor = QColor(PRIMARY_COLOR)

		self.initEndColor = QColor(endColor)

		self.endColor = QColor(PRIMARY_COLOR)
	
	def helper_function(self, color):

		self.setStyleSheet(f"background-color: {color.name()};color: {SECONDARY_COLOR}; font-size: 16px; border: none;")

		self._curColor = color
	
	def apply_color_animation(self, start_color, duration=1000):
		animation = QVariantAnimation(self)
		animation.setStartValue(start_color)
		animation.setEndValue(self.endColor)
		animation.setDuration(duration)
		animation.setEasingCurve(QEasingCurve.InCurve)

		animation.valueChanged.connect(functools.partial(self.helper_function))
		animation.start(QAbstractAnimation.DeleteWhenStopped)
	

	def enterEvent(self, event):
		self.endColor = QColor(self.initEndColor)
		self.apply_color_animation(self._curColor, 100)
		return super().enterEvent(event)
	
	def leaveEvent(self, event):
		self.endColor = QColor(PRIMARY_COLOR)
		self.apply_color_animation(self._curColor, 100)
		return super().leaveEvent(event)





class ExitDialog(QMessageBox):

	def __init__(self, txt = "You have unsaved changes!"):
		
		super().__init__()
		
		self.setText(txt)
		self.setInformativeText("Do you want to save your changes to the file?")
		self.saveButton = self.addButton("Save", QMessageBox.AcceptRole)
		self.setDefaultButton(self.saveButton)
		self.dontSaveButton = self.addButton("Don't save", QMessageBox.DestructiveRole)
		self.cancelButton = self.addButton("Cancel", QMessageBox.RejectRole)
		self.setEscapeButton(self.cancelButton)





class MainWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.setMinimumSize(720, 480)
		self.setWindowTitle("Text Editor")
		self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_FileIcon")))
		self.setStyleSheet(f"background-color: {PRIMARY_COLOR}")

		self.setWindowFlags(Qt.FramelessWindowHint | Qt.CustomizeWindowHint)
		
		
		if not ReadJsonFile(): self.settingsData = CreateJsonFile()
		else: self.settingsData = ReadJsonFile()

		self.font_ = QFont()
		self.font_.fromString(self.settingsData[0]["font"])


		self.textBuffer = ["", False]
		self.curFile = ""

		self.start = QPoint(0, 0)
		self.pressing = False
		
		
		self.menuBar = QMenuBar(self)

		self.menuBar.setStyleSheet(f"""
									QMenuBar {{
										background-color: {PRIMARY_COLOR};
										color: {SECONDARY_COLOR};
										font-size: 16px;
									}}
									QMenuBar::item:selected {{
										background-color: {HOVER_COLOR};
									}}
									""")

		self.menuBar.FileMenu = self.menuBar.addMenu("File")

		self.menuBar.FileMenu.NewFileAction = self.menuBar.FileMenu.addAction("New File...", QKeySequence("Ctrl+N"))
		self.menuBar.FileMenu.NewFileAction.triggered.connect(self.CreateFile)

		self.menuBar.FileMenu.OpenFileAction = self.menuBar.FileMenu.addAction("Open File...", QKeySequence("Ctrl+O"))
		self.menuBar.FileMenu.OpenFileAction.triggered.connect(self.OpenFile)

		self.menuBar.FileMenu.addSeparator()

		self.menuBar.FileMenu.CloseFileAction = self.menuBar.FileMenu.addAction("Close File", QKeySequence("Ctrl+Shift+C"))
		self.menuBar.FileMenu.CloseFileAction.triggered.connect(self.CloseFile)
		self.menuBar.FileMenu.CloseFileAction.setDisabled(True)

		self.menuBar.FileMenu.addSeparator()

		self.menuBar.FileMenu.SaveFileAction = self.menuBar.FileMenu.addAction("Save", QKeySequence("Ctrl+S"))
		self.menuBar.FileMenu.SaveFileAction.triggered.connect(self.SaveFile)
		self.menuBar.FileMenu.SaveFileAction.setDisabled(True)

		self.menuBar.FileMenu.SaveAsAction = self.menuBar.FileMenu.addAction("Save As...", QKeySequence("Ctrl+Shift+S"))
		self.menuBar.FileMenu.SaveAsAction.triggered.connect(self.SaveFileAs)

		self.menuBar.FileMenu.addSeparator()

		self.menuBar.FileMenu.ExitAction = self.menuBar.FileMenu.addAction("Exit", QKeySequence("Ctrl+Shift+Q"))
		self.menuBar.FileMenu.ExitAction.triggered.connect(self.ExitProgram)

		self.menuBar.FileMenu.setStyleSheet(f"""
											QMenu {{
												background-color: {PRIMARY_COLOR};
												color: {SECONDARY_COLOR};
											}}
											QMenu::item:selected {{
												background-color: {HOVER_COLOR};
											}}
											QMenu::item:disabled {{
												background-color: {PRIMARY_COLOR};
												color: black;
											}}
											""")


		self.menuBar.SettingsMenu = self.menuBar.addMenu("Settings")
		
		self.menuBar.SettingsMenu.ChangeFontAction = self.menuBar.SettingsMenu.addAction("Change Font...")
		self.menuBar.SettingsMenu.ChangeFontAction.triggered.connect(self.changeFont)
		self.menuBar.SettingsMenu.setStyleSheet(f"""
												QMenu {{
													background-color: {PRIMARY_COLOR};
													color: {SECONDARY_COLOR};
												}}
												QMenu::item:selected {{
													background-color: {HOVER_COLOR};
												}}
												""")
		
		self.menuBar.setFixedSize(self.menuBar.sizeHint())


		self.TextArea = QTextEdit(self)
		self.TextArea.setFont(self.font_)
		self.TextArea.setStyleSheet(f"""
									background-color: {BACKGROUND_COLOR};
									border: 1px solid {BORDER_COLOR};
									color: white;
									""")
		self.TextArea.textChanged.connect(self.CheckSaveBuffer)


		self.curFileDisplay = QLabel("No File opened")
		self.statusBar = QStatusBar(self)
		self.statusBar.addWidget(self.curFileDisplay)
		self.statusBar.setStyleSheet(f"""
									QStatusBar {{
										background-color: {PRIMARY_COLOR};
									}}
									QStatusBar::item {{
										border: none;
									}}
									QStatusBar QLabel {{
										color: {SECONDARY_COLOR};
									}}
									""")
		

		self.closeButton = FunctionButton(self, "X", "red")
		self.closeButton.setFixedSize(50, self.menuBar.sizeHint().height())
		self.closeButton.setStyleSheet(f"""
										QPushButton {{
											color: {SECONDARY_COLOR};
											border: none;
											font-size: 16px;
										}}
										""")
		self.closeButton.clicked.connect(self.triggerClose)

		self.minButton = FunctionButton(self, "─", HOVER_COLOR)
		self.minButton.setFixedSize(50, self.menuBar.sizeHint().height())
		self.minButton.setStyleSheet(f"""
										QPushButton {{
											color: {SECONDARY_COLOR};
											border: none;
											font-size: 16px;
										}}
										""")
		self.minButton.clicked.connect(self.triggerMin)
	

	
	def mousePressEvent(self, event):
		self.start = self.mapToGlobal(event.pos())
		self.pressing = True
	
	def mouseMoveEvent(self, event):
		if self.pressing:
			if self.isMaximized():
				return
			self.end = self.mapToGlobal(event.pos())
			self.movement = self.end - self.start
			self.move(self.mapToGlobal(self.movement))
			self.start = self.end
	
	def mouseReleaseEvent(self, event):
		self.pressing = False
	
	def resizeEvent(self, event):
		self.TextArea.setFixedSize(self.width(), self.height()-self.menuBar.height())
		self.TextArea.move(0, self.menuBar.height())
		self.statusBar.setFixedSize(self.width(), self.statusBar.sizeHint().height())
		self.statusBar.move(0, self.height()-self.statusBar.height())

		self.closeButton.move(self.width()-self.closeButton.width(), 0)
		self.minButton.move(self.width()-self.closeButton.width()-self.minButton.width(), 0)

		return super(MainWindow, self).resizeEvent(event)
	
	def closeEvent(self, event):
		if self.TextArea.toPlainText() == self.textBuffer[0]:
			self.close()
			return
		
		dialog = ExitDialog("Changes to the file have not been saved!")
		
		dialog.exec()

		if dialog.clickedButton() == dialog.cancelButton:
			return event.ignore()
		if dialog.clickedButton() == dialog.dontSaveButton:
			self.close()
			return super().closeEvent(event)
		if dialog.clickedButton() == dialog.saveButton:
			if self.TextArea.toPlainText() != self.textBuffer[0] and self.textBuffer[1] == False:
				ret = self.SaveFileAs()
				if ret == False: return event.ignore()
				self.close()
				return super().closeEvent(event)
			self.SaveFile()
			self.close()
			return super().closeEvent(event)
	

	@Slot()
	def triggerClose(self):
		self.close()
	
	@Slot()
	def triggerMin(self):
		self.showMinimized()
	

	
	@Slot()
	def ExitProgram(self):
		self.close()
	
	@Slot()
	def CreateFile(self):
		f = QFileDialog.getSaveFileName(self, "Create a new file", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f == "": return
		
		with open(f, "w", encoding="UTF-8") as fl:
			self.textBuffer = ["", True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
			self.menuBar.FileMenu.CloseFileAction.setDisabled(False)
	
	@Slot()
	def OpenFile(self):

		if self.TextArea.toPlainText() != self.textBuffer[0]:
			
			dialog = ExitDialog("You have unsaved changes!")
		
			dialog.exec()

			if dialog.clickedButton() == dialog.cancelButton:
				return
			if dialog.clickedButton() == dialog.dontSaveButton:
				pass
			if dialog.clickedButton() == dialog.saveButton:
				if self.textBuffer[1] == False:
					ret = self.SaveFileAs()
					if ret == False: return
					pass
				self.SaveFile()

		f = QFileDialog.getOpenFileName(self, "Open a file", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f == "": return

		with open(f, "r", encoding="UTF-8") as fl:
			content = fl.read()
			self.TextArea.setPlainText(content)
			self.textBuffer = [content, True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
			self.menuBar.FileMenu.CloseFileAction.setDisabled(False)
	
	@Slot()
	def CheckSaveBuffer(self):
		if self.textBuffer[1] == False: return
		
		if self.TextArea.toPlainText() != self.textBuffer[0]: self.menuBar.FileMenu.SaveFileAction.setDisabled(False)
		elif self.TextArea.toPlainText() == self.textBuffer[0]: self.menuBar.FileMenu.SaveFileAction.setDisabled(True)
	
	@Slot()
	def SaveFile(self):
		if self.textBuffer[1] == False: return

		with open(self.curFile, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer[0] = content
			self.menuBar.FileMenu.SaveFileAction.setDisabled(True)
	
	@Slot()
	def SaveFileAs(self):
		f = QFileDialog.getSaveFileName(self, "Save File As", filter="Text Files (*.txt);;All Files (*.*)")[0]
		if f == "": return False
		
		with open(f, "w", encoding="UTF-8") as fl:
			content = self.TextArea.toPlainText()
			fl.write(content)
			self.textBuffer = [content, True]
			self.curFile = f
			self.curFileDisplay.setText(self.curFile)
			self.menuBar.FileMenu.CloseFileAction.setDisabled(False)
	
	@Slot()
	def CloseFile(self):
		self.textBuffer = ["", False]
		self.curFile = ""
		self.TextArea.setText("")
		self.curFileDisplay.setText("No File opened")
		self.menuBar.FileMenu.CloseFileAction.setDisabled(True)
		self.menuBar.FileMenu.SaveFileAction.setDisabled(True)
	


	@Slot()
	def changeFont(self):
		font = QFontDialog.getFont()
		if font[0] == False: return
		self.TextArea.setFont(font[1])
		UpdateJsonFile(self.settingsData[1], font[1])
	




def ReadJsonFile():
	try:
		with open("settings.json", "r") as f:
			data = json.load(f)
			if "font" not in data.keys(): return False
			else: return [data, os.path.realpath(f.name)]
	except:
		return False

def CreateJsonFile():
	with open("settings.json", "w") as f:
		data = {
			"font": "Arial,16,-1,5,400,0,0,0,0,0,0,0,0,0,0,1,Standard"
		}
		json.dump(data, f, indent=4)
		return [data, os.path.realpath(f.name)]

def UpdateJsonFile(f, ctx):
	with open(f, "r") as fl:
		try:
			data = json.load(fl)
		except:
			CreateJsonFile()
			return
	
	data["font"] = ctx.toString()

	with open(f, "w") as fl:
		json.dump(data, fl, indent=4)