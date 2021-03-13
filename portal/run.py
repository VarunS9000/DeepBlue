from blog import app,socketio

if __name__=='__main__':
    #app.run(debug=True)
    app.run(host = '127.0.0.2',debug=True)
    socketio.run(app)
