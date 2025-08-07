from .extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Users(db.Model):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(25), nullable=False)

class Rooms(db.Model):
    __tablename__ = "Rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(25), nullable=False)

class RoomMembers(db.Model):
    __tablename__ = "RoomMembers"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, ForeignKey('Rooms.id'))
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))

    room = relationship('Rooms')
    user = relationship('Users')

class Messages(db.Model):
    __tablename__ = "Messages"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, ForeignKey('Rooms.id'))
    sender_id = db.Column(db.Integer, ForeignKey('Users.id'))
    content = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    room = relationship('Rooms')
    sender = relationship('Users')

class Friends(db.Model):
    __tablename__ = "Friends"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('Users.id'))
    friend_id = db.Column(db.Integer, ForeignKey('Users.id'))

    user = relationship('Users', foreign_keys=[friend_id])