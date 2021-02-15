import cv2
import os
import sys
os.chdir('C:\DeepBlue')
from darkflow.net.build import TFNet
import numpy as np
import requests
import json

path = os.path.join('C:\DeepBlue','bin\yolov2.weights')

options = {
    'model': 'C:\DeepBlue\cfg\yolo.cfg',
    'load': path,
    'threshold': 0.5,
    'gpu': 1.0
}

print('options: ',options)
try :
    tfnet = TFNet(options)
    colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
    url = 'http://192.168.1.22:8080/shot.jpg'
    #get the coods of the frame
    #rect = requests.post('/getCoords',data = {region: 'region'})
    while True:
        imgReq = requests.get(url)
        imgArr = np.array(bytearray(imgReq.content),dtype = np.uint8)
        frame = cv2.imdecode(imgArr,-1)
        frame = cv2.resize(frame,(640,480))
        print('frame: ',frame)
        #frame = frame[rect[1]:rect[3],rect[0]:rect[2]]

        results = tfnet.return_predict(frame)
        count = 0
        for color,result in zip(colors,results) :
            first = (result['topleft']['x'], result['topleft']['y'])
            second = (result['bottomright']['x'],result['bottomright']['y'])
            print('result: ',result)
            label = result['label']
            confidence = result['confidence']

            if label == 'person':
                count += 1
                text = '{}: {:.0f}%'.format(label, confidence * 100)
                frame = cv2.rectangle(frame, first, second, color, 3)
                frame = cv2.putText(frame,text,first,cv2.FONT_HERSHEY_COMPLEX, 1,(0,0,0),2)


        print('count: ',count)
        cv2.imshow('crow counting',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #capture.release()
            cv2.destroyAllWindows()
            break


except:
    print('error')
    cv2.destroyAllWindows()
