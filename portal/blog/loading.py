from darkflow.net.build import TFNet
import os

class Loading:
    tfnet='loading'
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
        
        
    