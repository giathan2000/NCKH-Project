
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QLabel, QMenu
from PyQt5 import QtCore
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *

app = QApplication([])

mainWindow = QMainWindow()

widget = QLabel("teststtststst")
widget.setObjectName("label")
widget.setStyleSheet(
    "#label { border: 5px solid red; background-color: yellow;}")
mainWindow.setCentralWidget(widget)

menu = QMenu(widget)
action = QAction("demo",widget)
action.
menu.addAction(action)

widget.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

mainWindow.setVisible(True)
mainWindow.show()
mainWindow.resize(1308, 857)


app.exec_()
