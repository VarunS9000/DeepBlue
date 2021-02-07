import os
import cv2
from blog.base_camera import BaseCamera
import numpy as np
import requests
from flask import request

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
        try:
            '''postUrl = 'http://127.0.0.1:5000/getIp'
            res = requests.post(postUrl,data={'hello':'hello'})
            print(res.text)
            ip_list = str(res.text).split(' ')
            for ip in ip_list:
                url = 'http://' + str(ip) + "/shot.jpg"'''


            url = 'http://'+ip+':'+port+'/shot.jpg'
            while True:
                print('inside while')
                img_req = requests.get(url)
                img_arr = np.array(bytearray(img_req.content),dtype = np.uint8)
                capture = cv2.imdecode(img_arr, -1)
                frame = cv2.resize(capture, (640, 480))
                cv2.imshow('url image',frame)
                yield cv2.imencode('.jpg',frame)[1].tobytes()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    capture.release()
                    cv2.destroyAllWindows()
                    break


        except:
            cv2.destroyAllWindows()
