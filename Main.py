
from PyQt5.QtWidgets import QApplication, QMainWindow
from ControllerViewCamera import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *

app = QApplication([])
 
mainWindow = QMainWindow()

controller = ControllerCameraView()

mainWindow.setCentralWidget(controller.cameraViewFrame)
mainWindow.resize(controller.cameraViewFrame.size())



mainWindow.setVisible(True)
app.exec_()

