from PyQt5.QtWidgets import QFrame
from CameraFactory import *
from ViewCamera import *


class ControllerCameraView:
    def __init__(self) -> None:

        self.cameraManager = CameraManager()
        self.cameraViewCreator = UiFrameCameraView()
        self.cameraViewFrame = QFrame()
        self.cameraViewCreator.setupUi(self.cameraViewFrame)
        self.cameraViewFrame.setVisible(True)

        if (self.cameraManager.availableCameraInfos[0] != None):
            print("notthing")
            if (self.cameraManager.cameraViewfnderList[0] == None):
                print("nothing2")
            self.cameraViewCreator.verticalLayout.addWidget(
                self.cameraManager.cameraViewfnderList[0])
