import secrets
from flask import render_template,url_for,flash,redirect,request,jsonify,Response
from blog import app,db,bcrypt
from blog.forms import Registration
from blog.models import CameraDb
from importlib import import_module
import os
from blog.camera_opencv import Camera
import requests
from darkflow.net.build import TFNet
import numpy as np
import cv2

@app.route("/",methods=['GET','POST'])
@app.route("/register",methods=['GET','POST'])
def register():
    form=Registration()
    if form.validate_on_submit():
        camera=CameraDb(ip=form.ip.data,region=form.region.data,port=form.port.data)
        db.session.add(camera)
        db.session.commit()
        flash(f'Account created for {form.ip.data}!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html',title='Register',form=form,values=CameraDb.query.all())



@app.route("/getCount",methods=['POST'])
def getCount():
    camera = CameraDb.query.all()

    try:
        path = os.path.join('D:\DeepBlue','bin\yolov2.weights')
        os.chdir('D:\DeepBlue')
        options = {
            'model': 'D:\DeepBlue\cfg\yolo.cfg',
            'load': path,
            'threshold': 0.5,
            'gpu': 1.0
        }
        tfnet = TFNet(options)
        count = 0
        print('camera: ',camera)
        for listItem in camera:
            print('listItem.ip: ',listItem.ip)
            print('port: ',listItem.port)
            url = 'http://'+listItem.ip+':'+str(listItem.port)+'/shot.jpg'
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
            results = tfnet.return_predict(frame)
            print('results: ',results)
            for result in results:
                if result['label'] == 'person':
                    count += 1
                     cam=CameraDb.query.filter(CameraDb.ip==listItem.ip and CameraDb.port==listItem.port).one()
                     cam.count=count
                     db.session.commit()
                    print('count: ',count)
            cap.release()


    except:
        print('error')

    return str(count)



@app.route('/camera',methods=['GET'])
def getCamera():
    ipAdd=request.args.get('ipAdd')
    region=request.args.get('region')
    port=request.args.get('port')

    return render_template('camera.html',title='Camera',ipAdd=ipAdd,region=region,port=port)

def gen(camera):
    """Video streaming generator function."""

    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/sendFrame',methods=['GET','POST'])
def sendFrame():
    # get the data and send success if inserted successfully in db else send error
    if request.method=='GET':
        print('inside sendFrame')
        cam=CameraDb.query.filter(CameraDb.ip==request.args.get('ip') and CameraDb.region==request.args.get('region')).one()
        cam.x1=request.args.get('x1')
        cam.y1=request.args.get('y1')
        cam.x2=request.args.get('x2')
        cam.y2=request.args.get('y2')
        print(cam)
        db.session.commit()
        return 'success'

    return 'error'


@app.route('/setCount',methods=['POST'])
def setCount():
    #print('inisde setCount bruh')
    req_data = request.get_json(force=True)
    count = req_data['count']
    print('req_data: ',req_data)
    #insert into db
    print('count: ',count)
    print('inside set count.. ',data.count)
    return

@app.route("/getIp",methods=['POST'])
def getIp():
    data = []
    print('inside getIP()')
    strm = ''
    for i in CameraDb.query.all():
        print('i.ip: ',i.ip)
        strm += i.ip + ' '
    print('now outside')
    return str(strm)

@app.route('/videoFeed',methods=['GET'])
def video_feed():

    ip=request.args.get('ipAdd')
    port=request.args.get('port')
    print(ip)
    print(port)

    return Response(gen(Camera(ip,port)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
