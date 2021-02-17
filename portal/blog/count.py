from blog.loading import Loading
import cv2
from blog.models import CameraDb
from blog import db
import requests
import numpy as np

import tensorflow
from tensorflow.keras.preprocessing import image
from PIL import Image





def countPeople(ip,port):
        camera = CameraDb.query.all()
        print('hello people')
        model = tensorflow.keras.models.load_model('C:/DeepBlue/portal/cnn.h5')




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
                label=result['label']
                if label == 'person':
                    img = frame[result['topleft']['x']:result['bottomright']['x'],result['topleft']['y']:result['bottomright']['y']]
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img=cv2.resize(img,(64,64))
                    im_pil = Image.fromarray(img)
                   
                    testImage = image.img_to_array(im_pil)
                    testImage = np.expand_dims(testImage, axis=0)
                    
                    
                    res = model.predict(testImage)
                    print(res)
                    if res[0][0] == 0:
                        print("it is a human")
                        count += 1
                        
                    else:
                        print("it is a mannequin")

                        text = 'mannequin'

            cam=CameraDb.query.filter(CameraDb.ip==ip and CameraDb.port==port).one()
            cam.count=count
            db.session.commit()
            cap.release()

        except:
            print('error')

        return count
