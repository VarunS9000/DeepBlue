import os
import cv2
from blog.base_camera import BaseCamera
from blog.models import CameraDb
import numpy as np
import requests
from flask import url_for,redirect
print(os.getcwd())
from darkflow.net.build import TFNet
import numpy as np
import requests
import json
import time
#from blog.__init__ import tfnet
class Camera(BaseCamera):
    video_source = 0


    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source


    @staticmethod
    def frames(ip,port):
        print('Frame Cam',ip)
        print('Frame Port',port)
        url = 'http://'+ip+':'+port+'/shot.jpg'
        url = str(url)
        print('url: ',url)
        imgReq = requests.get(url)
        imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
        frame = cv2.imdecode(imgArr,-1)
        frame = cv2.resize(frame,(640,480))
        print('frame: ',frame)
        #yield cv2.imencode('.jpg',frame)[1].tobytes()
        cv2.imshow('frame',frame)
        path = os.path.join('D:\DeepBlue','bin\yolov2.weights')
        os.chdir('D:\DeepBlue')
        options = {
            'model': 'D:\DeepBlue\cfg\yolo.cfg',
            'load': path,
            'threshold': 0.5,
            'gpu': 1.0
        }
        tfnet = TFNet(options)
        try:

            colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
            oldTime = time.time()
            print('oldTime',oldTime)
            while True:
                imgReq = requests.get(url)
                imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
                frame = cv2.imdecode(imgArr,-1)
                frame = cv2.resize(frame,(640,480))
                #frame = frame[rect[1]:rect[3],rect[0]:rect[2]]

                results = tfnet.return_predict(frame)
                print('got results')
                count = 0
                for color,result in zip(colors,results) :
                    first = (result['topleft']['x'], result['topleft']['y'])
                    second = (result['bottomright']['x'],result['bottomright']['y'])
                    print('result: ',result)
                    label = result['label']
                    confidence = result['confidence']

                    if label == 'person':
                        count += 1
                        label = label + '   count: ' + str(count)
                        text = '{}: {:.0f}%'.format(label, confidence * 100)
                        frame = cv2.rectangle(frame, first, second, color, 3)
                        frame = cv2.putText(frame,text,first,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)
                        cam=CameraDb.query.filter(CameraDb.ip==ip and CameraDb.port==port).one()
                        cam.count=count
                        db.session.commit()


                print('count: ',count)
                yield cv2.imencode('.jpg',frame)[1].tobytes()
                #cv2.imshow('crowd counting',frame)
                #yield cv2.imencode('.jpg',frame)[1].tobytes()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #capture.release()
                    BaseCamera.last_access=time.time()
                    return redirect(url_for('register'))
                    

                if time.time()-oldTime >= 10:
                    #insert in db count
                    oldTime = time.time()

        except:
            cv2.destroyAllWindows()
