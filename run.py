import eventlet
eventlet.monkey_patch()
from chat_app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, use_reloader=False)

