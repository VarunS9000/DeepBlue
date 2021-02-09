from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests
from darkflow.net.build import TFNet
import numpy as np
import cv2
import os
from flask_socketio import SocketIO

app=Flask(__name__)

app.config['SECRET_KEY']='22167761a9418bbd2e8af28881a557e2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
socketio = SocketIO(app)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

from blog import routes
