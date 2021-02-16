from blog.loading import Loading
import cv2
from blog.models import CameraDb
from blog import db
import requests
import numpy as np







def countPeople(ip,port):
        camera = CameraDb.query.all()
        print('hello people')
        
      

        try:
            
            
            
            count = 0
            print('camera: ',camera)
            print('listItem.ip: ',ip)
            print('port: ',port)
            url = 'http://'+ip+':'+str(port)+'/shot.jpg'
            url = str(url).replace(' ', '')
            print(url)
            '''print('inside url',url)
            imgReq = requests.get(url)'''
            cap = cv2.VideoCapture(url)
            _, frame = cap.read()
            cv2.imshow('frame',frame)
            '''print('imgReq',imgReq)
            imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
            print('imgArr',imgArr)
            frame = cv2.imdecode(imgArr,-1)
            print('frame: ',frame)
            frame = cv2.resize(imgArr,(640,480))'''
            print('Before results')
            results =Loading.tfnet.return_predict(frame)
            print('results: ',results)
            for result in results:
                if result['label'] == 'person':
                    count += 1

                    print('count: ',count)
            cam=CameraDb.query.filter(CameraDb.ip==ip and CameraDb.port==port).one()
            cam.count=count
            db.session.commit()
            cap.release()

        except:
            print('error')

        return count

        


