from datetime import datetime
from blog import db
from flask_login import UserMixin



class CameraDb(db.Model,UserMixin):
    ip=db.Column(db.String(15),primary_key=True)
    region=db.Column(db.String(20),nullable=False)
    count=db.Column(db.String(20),nullable=False,default=0)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Camera('{self.ip}',{self.region},{self.count}'{self.date_posted}')"
