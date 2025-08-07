from .extensions import socketio, db
from flask_socketio import join_room, leave_room, emit
from .models import Users, Rooms, RoomMembers, Messages
from .routes import session, get_private_room



@socketio.on("connect")
def register_connect():
    print("Client connected")

@socketio.on("join")
def on_join(data):
    user1 = data['user1']
    user2 = data['user2']
    room = get_private_room(user1, user2)

    found_room = Rooms.query.filter_by(room_name=room).first()

    if found_room:
        join_room(room)
    else:   
        new_room = Rooms(room_name = room)
        db.session.add(new_room)
        db.session.commit()

        user1_id = Users.query.filter_by(username=user1).first().id 
        user2_id = Users.query.filter_by(username=user2).first().id
        room_id = Rooms.query.filter_by(room_name=room).first().id

        new_room_member = RoomMembers(room_id=room_id, user_id=user1_id)
        db.session.add(new_room_member)
        db.session.commit()

        new_room_member2 = RoomMembers(room_id=room_id, user_id=user2_id)
        db.session.add(new_room_member2)
        db.session.commit()

        join_room(room)
    
    emit("joined_room", {'room' : room})

@socketio.on("leave")
def on_leave(data):
    room = data['room']
    leave_room(room)

@socketio.on("send_message")
def send_msg(data):
    sender_id = Users.query.filter_by(username = session['user']).first().id
    room_id = Rooms.query.filter_by(room_name = data['room']).first().id

    new_msg = Messages(room_id=room_id, sender_id=sender_id, content=data['message'])
    db.session.add(new_msg)
    db.session.commit()

    save_msg = [msg.id for msg in (db.session.query(Messages).filter_by(room_id=room_id).order_by(Messages.timestamp.desc()).limit(10).all())]

    db.session.query(Messages).filter(Messages.room_id == room_id, ~Messages.id.in_(save_msg)).delete(synchronize_session=False)
    db.session.commit()

    emit("receive_msg", {'sender' : session['user'], 'message' : data['message']}, room=data['room'])

