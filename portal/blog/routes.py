import secrets
from flask import render_template,url_for,flash,redirect,request,jsonify,Response
from blog import app,db,bcrypt
from blog.forms import Registration
from blog.models import CameraDb
from importlib import import_module
import os
from blog.camera_opencv import Camera



@app.route("/",methods=['GET','POST'])
@app.route("/register",methods=['GET','POST'])
def register():
    form=Registration()
    if form.validate_on_submit():
        camera=CameraDb(ip=form.ip.data,region=form.region.data)
        db.session.add(camera)
        db.session.commit()
        flash(f'Account created for {form.ip.data}!', 'success')
        return redirect(url_for('register'))
    return render_template('register.html',title='Register',form=form,values=CameraDb.query.all())

@app.route('/camera')
def getCamera():
    return render_template('camera.html',title='Camera')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/sendFrame')
def sendFrame():
    # get the data and send success if inserted successfully in db else send error
    return 'success'


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

@app.route('/videoFeed')
def video_feed():

    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
