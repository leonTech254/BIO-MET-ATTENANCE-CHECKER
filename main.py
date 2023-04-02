from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handle_message(data):
    print(data)


@socketio.on('my event')
def hello(data):
    print(data)


@socketio.on('from_flask')
def leon(data):
    print("hellow rolf")
    emit("name", {"name": "martin"}, broadcast=True)


@socketio.on("enrollUser")
def RegisterUser(data):
    pass


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
