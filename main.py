from PySide6.QtWidgets import QApplication
import function as fc
import sys



def main():
	
	app = QApplication()
	
	mW = fc.MainWindow()

	mW.show() #Comment

	sys.exit(app.exec())



if __name__ == '__main__':
	main()