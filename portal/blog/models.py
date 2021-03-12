from datetime import datetime
from blog import db
from flask_login import UserMixin



class CameraDb(db.Model,UserMixin):
    ip=db.Column(db.String(15),nullable=False)
    port=db.Column(db.String(5),nullable=False)
    region=db.Column(db.String(20),primary_key=True,nullable=False)
    count=db.Column(db.Integer,nullable=False,default=0)
    x1=db.Column(db.Float,nullable=False,default=0)
    y1=db.Column(db.Float,nullable=False,default=0)
    x2=db.Column(db.Float,nullable=False,default=0)
    y2=db.Column(db.Float,nullable=False,default=0)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"Camera('{self.ip}','{self.region}','{self.count}','{self.date_posted}','{self.x1}','{self.y1}','{self.x2}','{self.y2}')"


class HistoryDB(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    region=db.Column(db.String(20),db.ForeignKey('CameraDB.region'),nullable=False)
    count=db.Column(db.Integer,nullable=False,default=0)
    date_posted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"History('{self.region}','{self.count}','{self.date_posted}')"
