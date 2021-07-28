from typing import List
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *
from CameraFactory import *
from CVCamera import *


class CameraViewfiderFactory:

    def createCameraViewfider(self, camera: QCamera, startCamera=True) -> QCameraViewfinder:
        viewfinder = QCameraViewfinder()
        camera.setViewfinder(viewfinder)
        camera.setCaptureMode(QCamera.CaptureMode.CaptureStillImage)
        if(startCamera):
            camera.start()
        return viewfinder

    def createCameraObject(self, cameraInfo: QCameraInfo):
        return QCamera(cameraInfo)

    def availableCameras(self) -> List:
        return QCameraInfo.availableCameras()


class CameraManager:

    def __init__(self) -> None:
        self.creator = CameraViewfiderFactory()
        self.availableCameraInfos = self.creator.availableCameras()
        self.cameraList = list()
        self.cameraViewfnderList = list()
        for camareInfo in self.availableCameraInfos:
            camera = self.creator.createCameraObject(camareInfo)
            self.cameraList.append(camera)
            viewfinder = self.creator.createCameraViewfider(camera)
            self.cameraViewfnderList.append(viewfinder)

    def addCamera(self, addedCamera: QCamera):
        self.availableCameraInfos.append(addedCamera)
