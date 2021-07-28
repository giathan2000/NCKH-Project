import os
import cv2
import threading
from time import sleep
from PyQt5.QtGui import QImage, QPixmap
from ObjectProcessing.ObjectProcess import ObjectProcess
from PIL import Image


class CVCamera:

    VIDEO_TYPE = {
        'avi': cv2.VideoWriter_fourcc(*'XVID'),
        # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
        'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }

    def change_res(self, cap, width, height):
        cap.set(3, width)
        cap.set(4, height)

    STD_DIMENSIONS = {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }

    def get_dims(self, cap, res='1080p'):
        width, height = self.STD_DIMENSIONS["480p"]
        if res in self.STD_DIMENSIONS:
            width, height = self.STD_DIMENSIONS[res]
        # change the current caputre device
        # to the resulting resolution
        self.change_res(cap, width, height)
        return width, height

    def __init__(self, address, output="VideoOutput.avi", res="720p", processing: ObjectProcess = ObjectProcess()) -> None:
        self.video_capture = cv2.VideoCapture(address)
        print(self.video_capture.isOpened())
        self.output_video = None
        # cv2.VideoWriter(output, self.get_video_type(
        #     output), 20, self.get_dims(self.video_capture, res))
        self.processingObject: ObjectProcess = processing

    def recreateVideoWriter(self, output: str, res="720"):
        self.output_video = cv2.VideoWriter(output, self.get_video_type(
            output), 20, self.get_dims(self.video_capture, res))

    def processingImage(self, object: ObjectProcess):
        assert object != None
        self.processingObject = object

    def read(self, record=False, process=False) -> QPixmap:
        ret, self.frame = self.video_capture.read()
        self.frame = self.processingObject.processImage(self.frame)
        if record:
            self.recordReadFrame(process)
        return QPixmap(QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], self.frame.shape[1]*3, QImage.Format.Format_BGR888))

    def recordReadFrame(self, process=False):
        frame = self.frame
        if process:
            frame = self.processingObject.processImage(self.frame)
        self.output_video.write(frame)

    def recordCurrentFrame(self, process=False):
        if not self.video_capture.isOpened():
            raise IOError('Unable to load camera.')
        ret, frame = self.video_capture.read()
        if process:
            frame = self.processingObject.processImage(frame)
        self.output_video.write(frame)

    def get_video_type(self, filename=None):
        # filename, ext = os.path.splitext(filename)
        # if ext in self.VIDEO_TYPE:
        #     return self.VIDEO_TYPE[ext]
        return self.VIDEO_TYPE['avi']
