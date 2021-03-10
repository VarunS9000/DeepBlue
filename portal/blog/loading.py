from darkflow.net.build import TFNet
import os
from blog.models import CameraDb
import cv2
from blog import db

class Loading:
    tfnet='loading'
    done = False
    def load():
        path = os.path.join('C:\DeepBlue','bin\yolov2.weights')
        os.chdir('C:\DeepBlue')
        options = {
            'model': 'C:\DeepBlue\cfg\yolo.cfg',
            'load': path,
            'threshold': 0.5,
            'gpu': 1.0
        }
        return TFNet(options)

    def setVar():
        Loading.tfnet=Loading.load()
        Loading.done = True
