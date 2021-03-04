import secrets
from flask import render_template,url_for,flash,redirect,request,jsonify,Response,session
from blog import app,db,bcrypt,socketio
from blog.forms import Registration
from blog.models import CameraDb
from importlib import import_module
import os
from blog.camera_opencv import Camera
import requests
import numpy as np
import cv2
from flask_socketio import send, emit
from blog.loading import Loading
import blog.count as cp
import concurrent.futures
import threading


@socketio.on('coords')
def handle_json(json):
    print('received json: ' + str(json))
    print('simply coords: ',json)
    emit('success',json)



@app.route("/",methods=['GET','POST'])
def loadVar():

    return redirect(url_for('register'))
@app.route('/killCam',methods=['GET'])
def killCam():
    #kill the thread here....
    #return the svg file!!
    return yield()


@app.route("/loadTfnet",methods=['GET'])
def loadTfnet():
    Loading.setVar()
    form=Registration()
    if form.validate_on_submit():
        camera=CameraDb(ip=form.ip.data,region=form.region.data,port=form.port.data)
        db.session.add(camera)
        db.session.commit()
        flash(f'Account created for {form.ip.data}!', 'success')
        return redirect(url_for('register'))
    return str('/register')

@app.route("/register",methods=['GET','POST'])
def register():
    if Loading.tfnet=='loading':
        print('*******************************************************************************************************')
        return render_template('waves.html',title='Loading..',values = Loading)

    if Loading.done :
        form=Registration()
        if form.validate_on_submit():
            camera=CameraDb(ip=form.ip.data,region=form.region.data,port=form.port.data)
            db.session.add(camera)
            db.session.commit()
            flash(f'Account created for {form.ip.data}!', 'success')
            return redirect(url_for('register'))
        return render_template('register.html',title='Register',form=form,values=CameraDb.query.all(),mode=cp.mode)




@app.route('/advance',methods=['GET','POST'])
def advancedMode():

    cp.mode=not cp.mode

    if(not cp.mode and len(cp.threadList)>0):
        cp.threadStatus='stop'
        for x in cp.threadList:
            x.join()

    else:
        cp.threadStatus='running'

    camera = CameraDb.query.all()

    for x in camera:
        t=threading.Thread(target=cp.backgroundCount,args=[x.ip,x.port])
        t.start()
        cp.threadList.append(t)



    return redirect(url_for('register'))



@app.route("/user",methods=['GET'])
def user():
    return render_template('user.html', title='crowd counting mall')



@app.route("/getCount",methods=['POST','GET'])
def getCount():


    camera = CameraDb.query.all()
    counts=[]

    if(cp.mode):

        for c in camera:
            counts.append(c.count)

    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results=[executor.submit(cp.countPeople,x.ip,x.port) for x in camera]




        for f in concurrent.futures.as_completed(results):
            counts.append(f.result())





    print(sum(counts))

    return str(sum(counts))














@app.route('/camera',methods=['GET'])
def getCamera():

    ipAdd=request.args.get('ipAdd')
    region=request.args.get('region')
    port=request.args.get('port')

    if ipAdd==None:
        return redirect(url_for('register'))

    return render_template('camera.html',title='Camera',ipAdd=ipAdd,region=region,port=port)

def gen(camera):
    """Video streaming generator function."""

    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/sendFrame',methods=['GET'])
def sendFrame():
    # get the data and send success if inserted successfully in db else send error
    if request.method=='GET':
        print('inside sendFrame')
        print('***************************************************************************************************************************************************************************************************')
        cam=CameraDb.query.filter(CameraDb.ip==request.args.get('ip') and CameraDb.region==request.args.get('region')).one()
        cam.x1=request.args.get('x1')
        cam.y1=request.args.get('y1')
        cam.x2=request.args.get('x2')
        cam.y2=request.args.get('y2')
        print(cam)
        db.session.commit()

        return "success"


@app.route('/setCount',methods=['POST'])
def setCount():
    #print('inisde setCount bruh')
    q_data = request.get_json(force=True)
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
