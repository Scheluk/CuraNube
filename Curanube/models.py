from Curanube import db, login
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000), unique=True)
    confirmed = db.Column(db.Boolean)
    files = db.relationship('File', backref='User')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    owner_id =  db.Column(db.Integer, db.ForeignKey('user.id'))
    file_name = db.Column(db.String(1000))

class Shares(db.Model):
    __tablename__ = 'share'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    allowed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship("User", backref=backref("shares", cascade="all, delete-orphan"), primaryjoin="(Shares.owner_id==User.id)")
    file = relationship("File",  backref=backref("shares", cascade="all, delete-orphan"), primaryjoin="(Shares.file_id==File.id)")
