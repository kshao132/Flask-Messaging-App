from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models import Users, Friends, Messages, Rooms

main = Blueprint("main", __name__)

def get_private_room(user1, user2):
    return '_'.join(sorted([user1, user2]))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/signin', methods=["POST", "GET"])
def sign_in():
    if request.method == 'POST':
        action = request.form["action"]

        if action == 'submit':
            user = request.form['username']
            password = request.form['password']
            
            found_user = Users.query.filter_by(username=user).first()
            if found_user and password == found_user.password:
                    session["user"] = user
                    return redirect(url_for('main.friends'))
            else:
                flash('Username and/or Password do not exist')
                return render_template('signin.html')
        else:
            return redirect(url_for('main.index'))
    else:
        if "user" in session:
            return redirect(url_for('main.friends'))
        return render_template('signin.html')

@main.route('/signup', methods=["POST", "GET"])
def sign_up():
    if request.method == 'POST':
        action = request.form["action"]

        if action == 'submit':
            try:
                user = Users(username=request.form['username'], password=request.form['password'])
                db.session.add(user)
                db.session.commit()
                flash("Successfully Signed Up!")
                return redirect(url_for('main.index'))
            except IntegrityError:
                db.session.rollback()
                flash("Username already exists")
                return render_template('signup.html')
        else:
            return redirect(url_for('main.index'))
    else:
        return render_template('signup.html')

@main.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == 'POST':
        action = request.form['action']

        if action =='logout':
            return redirect(url_for('main.logout'))
        elif action == 'Enter':
            friend = request.form['friend']
            found_user = Users.query.filter_by(username=friend).first()
            if found_user:
                if found_user.username == session['user']:
                    flash("Cannot add yourself")
                    return redirect(url_for('main.friends'))
                found_user_id = found_user.id
                curr_user_id = Users.query.filter_by(username=session['user']).first().id
                friendship = Friends(user_id=curr_user_id, friend_id=found_user_id)
                db.session.add(friendship)
                db.session.commit()
                return(redirect(url_for('main.friends')))
            flash("User not found")
            return redirect(url_for('main.friends'))
        elif action == 'return':
            return redirect(url_for('main.friends'))
        else:
            return redirect(url_for('main.friends'))
    
    else:
        if "user" in session:
            username = session['user']
            username_id = Users.query.filter_by(username=username).first().id
            friends = Friends.query.filter_by(user_id=username_id).all()
            return render_template('friends.html', user=username, friendlist=friends)
        return redirect(url_for('main.signin'))

@main.route('/chat', methods=['POST', 'GET'])
def chat():
    print("ON CHAT")
    if request.method == "POST":
        return redirect(url_for('main.friends'))
    else:
        if "user" not in session:
            redirect(url_for('main.signin'))
        friend = request.args.get("user")
        found_user = Users.query.filter_by(username=friend).first()
        if found_user:
            room_name = get_private_room(friend, session['user'])
            found_room = Rooms.query.filter_by(room_name=room_name).first()
            if found_room:
                room_id = found_room.id
                past_messages = Messages.query.filter_by(room_id=room_id).order_by(Messages.timestamp.desc()).limit(10).all()
                past_messages.reverse()
                return render_template('chat.html', recipient=friend, curr_user=session["user"], displaymsg=past_messages)
            return render_template('chat.html', recipient=friend, curr_user=session["user"])
        flash("User not found")
        return render_template('chat.html')
        
@main.route('/logout')
def logout():  
    if "user" in session:
        session.pop("user", None)
        return redirect(url_for('main.sign_in'))
    else:
        return redirect(url_for('main.sign_in'))