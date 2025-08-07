from flask import Flask
import os
from .events import socketio
from .routes import main
from .extensions import db
from . import models

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'secret!'
    app.config["DEBUG"] = True
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI") or "sqlite:///instance/users.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(main)
    
    db.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    return app