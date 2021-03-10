import os
import cv2


import numpy as np
import requests
from flask import url_for,redirect,session
print(os.getcwd())
import numpy as np
import requests
import json
import time
import tensorflow

from tensorflow.keras.preprocessing import image
from PIL import Image
from darkflow.net.build import TFNet

cap = cv2.VideoCapture('sample1.mp4')
i=0




model = tensorflow.keras.models.load_model('D:/DeepBlue/portal/6.h5')

path= os.path.join('D:\DeepBlue','bin\yolov2.weights')
os.chdir('D:\DeepBlue')
options = {
    'model': 'D:\DeepBlue\cfg\yolo.cfg',
    'load': path,
    'threshold': 0.5,
    'gpu': 1.0
}

tfnet=TFNet(options)





#yield cv2.imencode('.jpg',frame)[1].tobytes()

#options = {
    #'model': 'C:\DeepBlue\cfg\yolo.cfg',
    #'load': path,
    #'threshold': 0.5,
    #'gpu': 1.0
#}

#tfnet = TFNet(options)







colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
oldTime = time.time()



vid_cod = cv2.VideoWriter_fourcc(*'mp4v')
resultK = cv2.VideoWriter('D:\DeepBlue\portal\demo1.mp4', vid_cod, 20.0, (640,640))
print('oldTime',oldTime)

while cap.isOpened():

    _,frame=cap.read()

    frame = cv2.resize(frame,(640,640))
    #frame = cv2.resize(frame,(640,420),interpolation=cv2.INTER_AREA)

    print('Before frame')


    results = tfnet.return_predict(frame)
    print('got results')
    count = 0
    for color,result in zip(colors,results) :
        first = (result['topleft']['x'], result['topleft']['y'])
        second = (result['bottomright']['x'],result['bottomright']['y'])
        #print('result: ',result)
        label = result['label']
        confidence = result['confidence']

        if label == 'person':
            print(frame)
            print(result['topleft']['x'],result['bottomright']['x'],result['topleft']['y'],result['bottomright']['y'])
            print(frame[result['topleft']['x']:result['bottomright']['x'],result['topleft']['y']:result['bottomright']['y']])
            img = frame[result['topleft']['x']:result['bottomright']['x'],result['topleft']['y']:result['bottomright']['y']]
            print(img,result)
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
                text = '{}: {:.0f}% c:{}'.format(label, confidence * 100, count)
            else:
                print("it is a mannequin")

                text = 'mannequin'+str(i)

            frame = cv2.rectangle(frame, first, second, color, 3)
            frame = cv2.putText(frame,text,first,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)
    cv2.imshow('frame',frame)
    resultK.write(frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cap.release()
        resultK.release()
        cv2.destroyAllWindows()
        break




    #print('count: ',count)
