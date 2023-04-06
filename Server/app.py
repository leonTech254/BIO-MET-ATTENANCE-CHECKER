from flask import Flask, redirect, request, send_file
from flask_cors import CORS
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
from io import BytesIO
import cv2 as cv
load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("Sqlite_path")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

face_cascade = cv.CascadeClassifier(
    "./OpencvCascades/haarcascade_frontalface_default.xml")


app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resorces={r'/*': {"orgins": '*'}})


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


@app.route('/api/register', methods=['POST', 'GET'])
def register():
    print("hello")
    check_face = False
    image_file = request.files['image']
    names = request.form['fname'] + " " + \
        request.form['mname'] + " " + request.form['lname']
    email = request.form['email']

    # read the image from file and do some processing
    image_bytes = BytesIO(image_file.read())
    image = cv.imdecode(np.frombuffer(
        image_bytes.getbuffer(), np.uint8), cv.IMREAD_COLOR)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in faces:
        check_face = True
        FaceID = Generate.ID()
        image_save = f"./Images/{FaceID}.png"
        cv.imwrite(image_save, image[y:y+h, x:x+w])
        train_response = train([image_save, FaceID])
        if train_response:
            data = Users(names=names, email=email, userId=FaceID)
            db.session.add(data)
            db.session.commit()
            print("hello")
        print(train_response)

    if check_face:
        return 'success'
    else:
        pass

    return "hello"


@app.route('/api/take_attendance')
def attendance_take():
    # print(data)
    name = Recongonation.Rec()
    print(name)
    return 'hello'


@app.route('/api/generateReport')
def leon():
    # print(data)
    users = Users.query.all()
    user_dict = {}
    for user in users:
        attendance = "Present"
        if user.present == "false":
            attendance = "Absent"
        user_dict[user.UserId] = user.Names+" "+attendance
    generate.report(data=user_dict)
    return send_file("./report.pdf", as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(host="0.0.0.0", debug=True)
