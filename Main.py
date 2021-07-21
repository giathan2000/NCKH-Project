
from PyQt5.QtWidgets import QApplication, QMainWindow
from ControllerViewCamera import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *

app = QApplication([])
 
mainWindow = QMainWindow()

controller = ControllerCameraView()

mainWindow.setCentralWidget(controller.cameraViewFrame)
mainWindow.setVisible(True)
mainWindow.show()
mainWindow.resize(1308, 857)

app.exec_()
