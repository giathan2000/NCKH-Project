
import sys
import PyQt5.QtMultimedia as qtm

from PyQt5.QtWidgets import *


def checkCameraAvailability() -> bool:
   print(len(qtm.QCameraInfo().availableCameras()))
   return (len(qtm.QCameraInfo().availableCameras()) > 0)


def window():

   camera = qtm.QCamera(0)
   camera.setCaptureMode(qtm.QCamera.CaptureMode.CaptureViewfinder)
   print("cammm : "+str(camera.isCaptureModeSupported(qtm.QCamera.CaptureMode.CaptureVideo)))
   camera.start()
   
   app = QApplication(sys.argv)
   w = QWidget()
   b = QLabel(w)
   b.setText("Hello World!")
   w.setGeometry(100, 100, 200, 50)
   b.move(50, 20)
   w.setWindowTitle("PyQt5")
   w.show()
   app.exec_()


print(checkCameraAvailability())
window()
