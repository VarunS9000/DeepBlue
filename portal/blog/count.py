from blog.loading import Loading
import cv2
from blog.models import CameraDb
from blog import db
import requests
import numpy as np


from tensorflow.keras.preprocessing import image
from PIL import Image
import tensorflow
model = tensorflow.keras.models.load_model('D:/DeepBlue/portal/cnn.h5')




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
                if label == 'person':
                    img = frame[result['topleft']['x']:result['bottomright']['x'],result['topleft']['y']:result['bottomright']['y']]
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    im_pil = Image.fromarray(img)
                    testImage = image.load_img('11.png',target_size=(64,64))
                    testImage = image.img_to_array(testImage)
                    testImage = np.expand_dims(testImage, axis=0)
                    result = model.predict(testImage)
                    print(result)
                    if result[0][0] == 0:
                        print("it is a human")
                        count += 1
                        label = 'person'
                        text = '{}: {:.0f}%'.format(label, confidence * 100)
                    else:
                        print("it is a mannequin")

                        text = 'mannequin'


                    frame = cv2.rectangle(frame, first, second, color, 3)
                    frame = cv2.putText(frame,text,first,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)
            cam=CameraDb.query.filter(CameraDb.ip==ip and CameraDb.port==port).one()
            cam.count=count
            db.session.commit()
            cap.release()

        except:
            print('error')

        return count
