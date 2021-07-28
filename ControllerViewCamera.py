from typing import Dict
from PyQt5.QtWidgets import QAction, QDialog, QFrame, QLabel, QLineEdit, QPushButton, QToolBox, QToolButton, QWidget
from PyQt5.QtMultimedia import *
from CameraFactory import *
from ViewCamera import *
from CVCamera import *
import threading as thr
import AddRemoteCameraDialog
import AlertDialog
import types
import numpy as np
from PIL import Image


class ControllerCameraView:
    def __init__(self) -> None:

        # self.cameraManager = CameraManager()
        self.__setupUI()
        self.__mappingItem()

        self.cameraList: Dict[str, CVCamera] = {}

        self.taskAssignment: Dict[QLabel, CVCamera] = {}
        self.threadList: Dict[QLabel, thr.Thread] = {}
        self.isActiveLabel: Dict[QLabel, bool] = {}
        self.recordCamera: Dict[QLabel, bool] = {}
        self.__configEvent()
        self.setRecordInterface(self.labelList[3].parentWidget(), True)

    def __setupUI(self):
        self.cameraViewCreator = UiFrameCameraView()
        self.cameraViewFrame = QFrame()
        self.cameraViewCreator.setupUi(self.cameraViewFrame)
        self.cameraViewFrame.setVisible(True)

        self.addCameraDialog = QDialog(self.cameraViewFrame)
        self.addCameraDialogCreator = AddRemoteCameraDialog.AddRemoteCameraDialog()
        self.addCameraDialogCreator.setupUi(self.addCameraDialog)
        self.addCameraDialog.setModal(True)

        self.alertDialog = AlertDialog.AlertDialog()

        for item in self.__returnCameraIndexes():
            self.addCameraDialogCreator.cameraListComboBox.addItem(str(item))

    def __mappingItem(self):

        self.labelList = [self.cameraViewCreator.label,
                          self.cameraViewCreator.label_2,
                          self.cameraViewCreator.label_3,
                          self.cameraViewCreator.label_4,
                          self.cameraViewCreator.label_5,
                          self.cameraViewCreator.label_6]
        self.addCamerapushButtonList: List[QPushButton] = [self.cameraViewCreator.addCamerapushButton,
                                                           self.cameraViewCreator.addCamerapushButton_2,
                                                           self.cameraViewCreator.addCamerapushButton_3,
                                                           self.cameraViewCreator.addCamerapushButton_4,
                                                           self.cameraViewCreator.addCamerapushButton_5,
                                                           self.cameraViewCreator.addCamerapushButton_6]

        self.warningSettingpushButtonList: List[QPushButton] = [self.cameraViewCreator.warningSettingpushButton,
                                                                self.cameraViewCreator.warningSettingpushButton_2,
                                                                self.cameraViewCreator.warningSettingpushButton_2,
                                                                self.cameraViewCreator.warningSettingpushButton_2,
                                                                self.cameraViewCreator.warningSettingpushButton_2,
                                                                self.cameraViewCreator.warningSettingpushButton_2]

        self.recordPushButtonList: List[QPushButton] = [self.cameraViewCreator.recordPushButton,
                                                        self.cameraViewCreator.recordPushButton_2,
                                                        self.cameraViewCreator.recordPushButton_3,
                                                        self.cameraViewCreator.recordPushButton_4,
                                                        self.cameraViewCreator.recordPushButton_5,
                                                        self.cameraViewCreator.recordPushButton_6]

        self.stopRecordPushButtonList: List[QPushButton] = [self.cameraViewCreator.stopRecordPushButton,
                                                            self.cameraViewCreator.stopRecordPushButton_2,
                                                            self.cameraViewCreator.stopRecordPushButton_3,
                                                            self.cameraViewCreator.stopRecordPushButton_4,
                                                            self.cameraViewCreator.stopRecordPushButton_5,
                                                            self.cameraViewCreator.stopRecordPushButton_6]

        self.filenameLineEditList: List[QLineEdit] = [self.cameraViewCreator.filenameLineEdit,
                                                      self.cameraViewCreator.filenameLineEdit_2,
                                                      self.cameraViewCreator.filenameLineEdit_3,
                                                      self.cameraViewCreator.filenameLineEdit_4,
                                                      self.cameraViewCreator.filenameLineEdit_5,
                                                      self.cameraViewCreator.filenameLineEdit_6]

        self.pathLineEditList: List[QLineEdit] = [self.cameraViewCreator.pathLineEdit,
                                                  self.cameraViewCreator.pathLineEdit_2,
                                                  self.cameraViewCreator.pathLineEdit_3,
                                                  self.cameraViewCreator.pathLineEdit_4,
                                                  self.cameraViewCreator.pathLineEdit_5,
                                                  self.cameraViewCreator.pathLineEdit_6]

        self.choosePathToolButtonList: List[QToolButton] = [self.cameraViewCreator.choosePathToolButton,
                                                            self.cameraViewCreator.choosePathToolButton_2,
                                                            self.cameraViewCreator.choosePathToolButton_3,
                                                            self.cameraViewCreator.choosePathToolButton_4,
                                                            self.cameraViewCreator.choosePathToolButton_5,
                                                            self.cameraViewCreator.choosePathToolButton_6]

        self.disconnectButtonList: List[QPushButton] = [self.cameraViewCreator.disconnectPushButton,
                                                        self.cameraViewCreator.disconnectPushButton_2,
                                                        self.cameraViewCreator.disconnectPushButton_3,
                                                        self.cameraViewCreator.disconnectPushButton_4,
                                                        self.cameraViewCreator.disconnectPushButton_5,
                                                        self.cameraViewCreator.disconnectPushButton_6, ]

        self.toolBoxMap: Dict[QLabel, QToolBox] = {self.cameraViewCreator.label: self.cameraViewCreator.toolBox,
                                                   self.cameraViewCreator.label_2: self.cameraViewCreator.toolBox_2,
                                                   self.cameraViewCreator.label_3: self.cameraViewCreator.toolBox_3,
                                                   self.cameraViewCreator.label_4: self.cameraViewCreator.toolBox_4,
                                                   self.cameraViewCreator.label_5: self.cameraViewCreator.toolBox_5,
                                                   self.cameraViewCreator.label_6: self.cameraViewCreator.toolBox_6}

    def __configEvent(self):
        # Thêm sự kiện nhấn chuột cho mỗi frame camera
        for btn in self.addCamerapushButtonList:
            # temp:function = self.copy_func(self.__addRemoteCameraAction)
            btn.clicked.connect(lambda: self.__addRemoteCameraAction())

        for btn in self.disconnectButtonList:
            btn.clicked.connect(lambda: self.__disconnectCameraAction())

        for btn in self.choosePathToolButtonList:
            btn.clicked.connect(lambda: self.__fileChooserAction())

        for btn in self.recordPushButtonList:
            btn.clicked.connect(lambda: self.__startRecordAction())

        for btn in self.stopRecordPushButtonList:
            btn.clicked.connect(lambda: self.__stopRecord())

    def __addRemoteCameraAction(self):
        btn = self.cameraViewFrame.sender()
        self.addCameraDialog.setVisible(True)
        # xử lí khi thêm remotecamera
        try:
            self.addCameraDialogCreator.okayPushButton.clicked.disconnect()
        except Exception:
            pass
        self.addCameraDialogCreator.okayPushButton.clicked.connect(
            lambda: self.__addRemoteCameraActionDialogButton(btn))

        # Xứ lí khi thêm localcamera
        try:
            self.addCameraDialogCreator.okayPushButton_2.clicked.disconnect()
        except Exception:
            pass
        self.addCameraDialogCreator.okayPushButton_2.clicked.connect(
            lambda: self.__addLocalCameraActionDialogButton(btn))

    def __addRemoteCameraActionDialogButton(self, btnInCameraLabel: QPushButton):
        # Them hoac thay the camera
        index = self.addCamerapushButtonList.index(btnInCameraLabel)

        nameCamera = self.addCameraDialogCreator.nameCameraLineEdit.text()
        if not nameCamera:
            self.alertDialog.tenCameraKhongHopLe()
            return
        link = self.addCameraDialogCreator.urlLineEdit.text()
        passw = self.addCameraDialogCreator.passwordLineEdit.text()
        username = self.addCameraDialogCreator.usernameLineEdit.text()
        acesslink = link
        if(passw and username):
            acesslink = link[0:7] + username + ":" + passw + "@" + link[7:]
        self.newCamera(nameCamera, acesslink)
        self.runCamera(nameCamera, self.labelList[index])
        self.addCameraDialog.setVisible(False)

    def __addLocalCameraActionDialogButton(self, btnInCameraLabel: QPushButton):
        index = self.addCamerapushButtonList.index(btnInCameraLabel)
        nameCamera = self.addCameraDialogCreator.nameCameraLineEdit_2.text()
        if not nameCamera:
            self.alertDialog.tenCameraKhongHopLe()
            return
        indexcam = self.addCameraDialogCreator.cameraListComboBox.currentText()
        self.newCamera(nameCamera, int(indexcam))
        self.runCamera(nameCamera, self.labelList[index])
        self.addCameraDialog.setVisible(False)

    def __disconnectCameraAction(self):
        btn = self.cameraViewFrame.sender()
        intdex = self.disconnectButtonList.index(btn)
        self.stopCamera(self.labelList[intdex])

    def __fileChooserAction(self):
        path = str(QtWidgets.QFileDialog.getExistingDirectory())
        btn = self.cameraViewFrame.sender()
        index = self.choosePathToolButtonList.index(btn)
        self.pathLineEditList[index].setText(path)

    def __returnCameraIndexes(self):
        # checks the first 10 indexes.
        index = 0
        arr = []
        i = 20
        while i > 0:
            cap = cv2.VideoCapture(index)
            if cap.read()[0]:
                arr.append(index)
                cap.release()
            index += 1
            i -= 1
        return arr

    def printTest(self, e: QtGui.QKeyEvent):

        print("okay nhe")

    def printTest2(self):

        print("okay nhe 22")

    def setNameCamera(self, name: str, label: QLabel):
        _translate = QtCore.QCoreApplication.translate
        toolbox = self.toolBoxMap[label]
        wparent = label.parentWidget()
        toolbox.setItemText(toolbox.indexOf(wparent),
                            _translate("Frame", name))

    def newCamera(self, name, address, output="video.avi", res="720p", processing: ObjectProcess = ObjectProcess()):
        self.cameraList[name] = CVCamera(address, output, res, processing)

    def runCamera(self, name: str, label: QLabel):
        self.setNameCamera(name, label)
        self.taskAssignment[label] = self.cameraList[name]
        self.isActiveLabel[label] = True
        self.recordCamera[label] = False
        t = thr.Thread(target=self.__runCamera, args=(name, label,))
        t.setDaemon(True)
        t.start()
        self.threadList[label] = t

    def __runCamera(self, name: str, label: QLabel):

        camera: CVCamera = self.cameraList[name]
        if not camera.video_capture.isOpened():
            raise IOError('Unable to load camera.')

        while self.isActiveLabel[label]:
            pixmap = camera.read().scaled(label.width(), label.height(), aspectRatioMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                          transformMode=QtCore.Qt.TransformationMode.FastTransformation)
            if self.recordCamera[label]:
                camera.recordReadFrame()
            else:
                if not camera.output_video:
                    try:
                        camera.output_video.release()
                        camera.output_video = None
                    except:
                        pass
            label.setPixmap(pixmap)

        camera.video_capture.release()
        try:
            camera.output_video.release()
        except:
            pass
        self.noCameraImageDisplay(label)

    def __startRecordAction(self):
        btn = self.cameraViewFrame.sender()
        index = self.recordPushButtonList.index(btn)
        label = self.labelList[index]

        filename = self.filenameLineEditList[index].text()
        path = self.pathLineEditList[index].text()
        if not filename or not path:
            self.alertDialog.tenFileHoacĐuongDanKhongHopLe()
            return
        else:
            self.__startRecord(label, filename=filename, dir=path)
            self.setRecordInterface(label.parentWidget().parentWidget().parentWidget(), True)

    def __startRecord(self, label: QLabel, process=False, filename=None, dir=None):
        if filename or dir:
            path = filename
            self.taskAssignment[label].recreateVideoWriter(path)
        self.recordCamera[label] = True

    def __stopRecord(self):
        btn = self.cameraViewFrame.sender()
        index = self.stopRecordPushButtonList.index(btn)
        label = self.labelList[index]
        self.stopRecord(label)

    def stopRecord(self, label: QLabel):
        self.recordCamera[label] = False
        try:
            self.taskAssignment[label].output_video.release()
        except: pass
        self.taskAssignment[label].output_video = None
        self.setRecordInterface(label.parentWidget().parentWidget().parentWidget(), False)
        print("stopre")

    def stopCamera(self, label: QLabel):
        self.isActiveLabel[label] = False

    def deleteCamera(self, name):
        if self.taskAssignment[name] != None:
            del self.taskAssignment[name]

    def test(self):
        self.newCamera("webcam", 0)
        self.runCamera("webcam", self.labelList[0])

    def copy_func(self, f, name=None):
        fn = types.FunctionType(f.__code__, f.__globals__, name or f.__name__,
                                f.__defaults__, f.__closure__)
        # in case f was given attrs (note this dict is a shallow copy):
        fn.__dict__.update(f.__dict__)
        return fn

    def noCameraImageDisplay(self, label: QLabel):

        frame = cv2.imread("img/nocamera.jpg")
        pixmap = QPixmap(QImage(
            frame.data, frame.shape[1], frame.shape[0], frame.shape[1]*3, QImage.Format.Format_BGR888))
        label.setPixmap(pixmap)

    def setRecordInterface(self, widget: QWidget, isRecord=False):
        name = widget.objectName()
        if isRecord:
            widget.setStyleSheet('#'+name+'{  border: 4px solid red; }')
        else:
            widget.setStyleSheet('#'+name+'{  border: 1px solid black; }')
