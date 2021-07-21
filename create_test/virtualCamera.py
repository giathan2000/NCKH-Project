from pyvirtualcam import *
import PIL.Image as Image
import numpy as np

cam1 = Camera(720,214,  20, print_fps=True)
cam2 = Camera(540,960,  20, print_fps=True)
cam3 = Camera(720,533,  20, print_fps=True)
img1  = np.array(Image.open("D:/Drive/PythonProject/NCKH-Project/create_test/1.jpg"))
img2  = np.array(Image.open("D:/Drive/PythonProject/NCKH-Project/create_test/2.jpg"))
img3  = np.array(Image.open("D:/Drive/PythonProject/NCKH-Project/create_test/3.jpg"))

while True :
   cam1.send(img1)
   cam2.send(img2)
   cam3.send(img3)
