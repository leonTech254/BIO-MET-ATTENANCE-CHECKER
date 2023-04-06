from flask import Flask, redirect, request, send_file
from flask_socketio import SocketIO, emit, join_room, leave_room
from generate_id import Generate
import numpy as np
from face_rec import Recongonation

from Models.db import db
from Models.model import Users
import os
from dotenv import load_dotenv
from generateReport import generate
import base64
import cv2 as cv
load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("Sqlite_path")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

face_cascade = cv.CascadeClassifier(
    "./OpencvCascades/haarcascade_frontalface_default.xml")


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handle_message(data):
    print(data)


@socketio.on('my event')
def hello(data):
    print(data)


def train(Datalist):
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    try:
        # Load the existing model if it exists
        face_recognizer.read('model.yml')
    except cv.error:
        # If the model doesn't exist, create a new one
        pass
    image = cv.imread(Datalist[0])
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    images = [gray]
    labels = [int(Datalist[1])]
    labels = np.array(labels)

    face_recognizer.update(images, labels)
    face_recognizer.save('model.yml')
    print("Training complete")
    return True


@socketio.on('register')
def register(data):
    check_face = False
    contents = data['credentials']
    image_data = data['credentials']['image']
    names = contents['fname']+" "+contents['mname']+" "+contents['lname']
    email = contents['email']

    # # convert base64-encoded image data to bytes
    image_bytes = base64.b64decode(image_data.split(',')[1])

    # save the image to a file
    FaceID = Generate.ID()
    image_save = f"./Images/{FaceID}.png"
    with open(image_save, 'wb') as f:
        f.write(image_bytes)
    image = cv.imread(image_save)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        # cv.rectangle(rotated_image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #
        # cv.imwrite(image_save, rotated_image)
        check_face = True
        train_response = train([image_save, FaceID])
        if train_response:
            data = Users(names=names, email=email, userId=FaceID)
            db.session.add(data)
            db.session.commit()
            print("hello")
        print(train_response)
    if check_face:
        emit("name", {"message": "success"}, broadcast=True)
    else:
        emit("name", {"message": "false"}, broadcast=True)


@socketio.on('take_attendance')
def leon(data):
    print(data)
    name = Recongonation.Rec()
    print(name)


@socketio.on('generateReport')
def leon(data):
    print(data)
    users = Users.query.all()
    user_dict = {}
    for user in users:
        if user.present == "false":
            attendance = "Absent"
        user_dict[user.UserId] = user.Names+" "+attendance
    generate.report(data=user_dict)
    send_file("./report.pdf", as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    socketio.run(app, host="0.0.0.0", debug=True)
