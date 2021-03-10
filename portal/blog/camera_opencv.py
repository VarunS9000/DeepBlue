import os
import cv2
from blog import db
from blog.base_camera import BaseCamera
from blog.models import CameraDb
import numpy as np
import requests
from flask import url_for,redirect,session
print(os.getcwd())
import numpy as np
import requests
import json
import time
import tensorflow
from blog.loading import Loading
from tensorflow.keras.preprocessing import image
from PIL import Image
import blog.count as cp


#from blog.__init__ import tfnet
class Camera(BaseCamera):
    video_source = 0
    threadStatus='running'
    back_port=''



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
        model = tensorflow.keras.models.load_model('C:/DeepBlue/portal/6.h5')
        print('Frame Cam',ip)
        print('Frame Port',port)
        if(port is not None):
            Camera.back_port=port

        else:
            port=Camera.back_port

        
        
        url = 'http://'+ip+':'+port+'/shot.jpg'
        url = str(url)
        #print('rect: ',rect)
        print('url: ',url)
        imgReq = requests.get(url)
        imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
        frame = cv2.imdecode(imgArr,-1)
        frame = cv2.resize(frame,(640,480))
        print('frame: ',frame)
        #yield cv2.imencode('.jpg',frame)[1].tobytes()
        #cv2.imshow('frame',frame)
        #options = {
            #'model': 'C:\DeepBlue\cfg\yolo.cfg',
            #'load': path,
            #'threshold': 0.5,
            #'gpu': 1.0
        #}

        #tfnet = TFNet(options)



        try:

            colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
            oldTime = time.time()
            print('oldTime',oldTime)
            Camera.threadStatus='start'
            while True:
                imgReq = requests.get(url)
                imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
                frame = cv2.imdecode(imgArr,-1)
                frame = cv2.resize(frame,(640,640))
                cam=CameraDb.query.filter(CameraDb.ip==ip and CameraDb.port==port).one()
                rect=[]
                rect.append(cam.x1)
                rect.append(cam.y1)
                val=cp.frameSlice(cam.x1,cam.x2,cam.y1,cam.y2)
                rect.append(cam.x1+val)
                rect.append(cam.y1+val)
                rect = [int(x) for x in rect]
                print('rect: ',rect)
                if rect != [0,0,0,0]:
                    #print('inside rect !=')
                    frame = frame[rect[0]:rect[2],rect[1]:rect[3]]

                #print('frame: ',frame)
                print('Before frame')
                results = Loading.tfnet.return_predict(frame)
                print('got results')
                count = 0
                for color,result in zip(colors,results) :
                    first = (result['topleft']['x'], result['topleft']['y'])
                    second = (result['bottomright']['x'],result['bottomright']['y'])
                    #print('result: ',result)
                    label = result['label']
                    confidence = result['confidence']

                    if label == 'person':
                        img = frame[result['topleft']['x']:result['bottomright']['x'],result['topleft']['y']:result['bottomright']['y']]
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        img=cv2.resize(img,(64,64))
                        print('pass1')
                        im_pil = Image.fromarray(img)
                        print('pass2')


                        testImage = image.img_to_array(im_pil)
                        testImage = np.expand_dims(testImage, axis=0)
                        res = model.predict(testImage)
                        if res[0][0] == 0:
                            print("it is a human")
                            count += 1
                            label = 'person'
                            text = '{}: {:.0f}% count:{}'.format(label, confidence * 100, count)
                        else:
                            print("it is a mannequin")

                            text = 'mannequin'

                        frame = cv2.rectangle(frame, first, second, color, 3)
                        frame = cv2.putText(frame,text,first,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)


                #print('count: ',count)
                yield cv2.imencode('.jpg',frame)[1].tobytes()
                #cv2.imshow('crowd counting',frame)
                #yield cv2.imencode('.jpg',frame)[1].tobytes()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #capture.release()
                    BaseCamera.last_access=time.time()
                    #return redirect(url_for('register'))
                    print('before break')
                    #break
                    return


                if time.time()-oldTime >= 10:
                    cam.count=count
                    db.session.commit()
                    oldTime = time.time()

                if Camera.threadStatus=='stop':
                    break

        except:
            cv2.destroyAllWindows()
