print('1')
import cv2
from darkflow.net.build import TFNet
print('2')
import numpy as np
import time
import requests
import json
options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.2,
    'gpu': 1.0
}
print('abc')
try:
    print('inside try')
    tfnet = TFNet(options)
    print('3')
    colors = [tuple(255 * np.random.rand(3)) for _ in range(10)]
    postUrl = 'http://127.0.0.1:5000/getIp'
    res = requests.post(postUrl,data={'hello':'hello'})
    print(res.text)
    temp = str(res.text).split(' ')
    print(temp)
    url = 'http://192.168.43.1:8080/shot.jpg'
    #capture0 = cv2.VideoCapture(0)
    #capture0.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    #capture0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    drawing = False
    mode = True
    (ix, iy) = (-1, -1)
    windowName1 = 'frame_1'
    windowName2 = 'frame_2'
    rect = (0,0,0,0)
    startPoint = False
    endPoint = False
    def draw_shape(event, x, y, flags, param):
        global rect,startPoint,endPoint

        # get mouse click
        if event == cv2.EVENT_LBUTTONDOWN:

            if startPoint == True and endPoint == True:
                startPoint = False
                endPoint = False
                rect = (0, 0, 0, 0)

            if startPoint == False:
                rect = (x, y, 0, 0)
                startPoint = True
            elif endPoint == False:
                rect = (rect[0], rect[1], x, y)
                endPoint = True
    while True:
        print('while ke andar')
        stime = time.time()
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content),dtype = np.uint8)
        capture0 = cv2.imdecode(img_arr, -1)
        capture0 = cv2.resize(capture0, (640, 480))
        #cv2.imshow('cam', capture0)
        #ret0, frame0 = cv2.imread(capture0,0)
        ret, frame = capture.read()

        '''results1 = tfnet.return_predict(frame)
        for color1, result1 in zip(colors, results1):
            print('inside for of video cam')
            tl = (result1['topleft']['x'], result1['topleft']['y'])
            br = (result1['bottomright']['x'], result1['bottomright']['y'])
            label = result1['label']
            confidence = result1['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            frame = cv2.rectangle(frame, tl, br, color1, 5)
            frame = cv2.putText(
                frame, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        results = tfnet.return_predict(capture0)
        for color, result in zip(colors, results):
            tl = (result['topleft']['x'], result['topleft']['y'])
            br = (result['bottomright']['x'], result['bottomright']['y'])
            label = result['label']
            confidence = result['confidence']
            text = '{}: {:.0f}%'.format(label, confidence * 100)
            capture0 = cv2.rectangle(capture0, tl, br, color, 5)
            capture0 = cv2.putText(
                capture0, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        print('FPS {:.1f}'.format(1 / (time.time() - stime)))'''


        cv2.namedWindow(windowName1)
        cv2.namedWindow(windowName2)
        cv2.setMouseCallback(windowName1,draw_shape)
        cv2.setMouseCallback(windowName2,draw_shape)

        if startPoint == True and endPoint == True:
            print('inside of if')
            #frame = cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (255, 0, 255), -1)
            x = capture0[rect[1]:rect[3],rect[0]:rect[2]]
            #print('x: ',x)
            #img_arr = np.array(bytearray(x.content),dtype = np.uint8)
            #x = cv2.imdecode(x, -1)
            #capture0 = cv2.resize(capture0, (640, 480))
            x = cv2.resize(x, (640, 480))
            results1 = tfnet.return_predict(x)
            count = 0
            for color1, result1 in zip(colors, results1):
                print('inside for of video cam')
                tl = (result1['topleft']['x'], result1['topleft']['y'])
                br = (result1['bottomright']['x'], result1['bottomright']['y'])
                label = result1['label']
                confidence = result1['confidence']
                if label == 'person':
                    count += 1
                text = '{}: {:.0f}%'.format(label, confidence * 100) + '   count: '+ str(count)
                x = cv2.rectangle(x, tl, br, color1, 5)
                x = cv2.putText(
                    x, text, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            print('FPS {:.1f}'.format(1 / (time.time() - stime)))
            print('count: ',count)
            #cv2.destroyAllWindows()
            cv2.imshow('x',x)
        cv2.imshow(windowName1, capture0)
        cv2.imshow(windowName2, frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            capture.release()
            cv2.destroyAllWindows()
            break

except:
    cv2.destroyAllWindows()
