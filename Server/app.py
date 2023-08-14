from flask import Flask, redirect, request, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from generate_id import Generate
import numpy as np
from face_rec import Recongonation,EnrollFace

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
output_dir = 'Images'
os.makedirs(output_dir, exist_ok=True)

def train(Datalist):
    face_recognizer = cv.face.LBPHFaceRecognizer_create()
    try:
        face_recognizer.read('model.yml')
    except cv.error:
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
    try:
        check_face = False
        image_file = request.files['image']
        names = f"{request.form['fname']} {request.form['mname']} {request.form['lname']}"
        email = request.form['email']

        # Read the image from the file and perform processing
        image_bytes = BytesIO(image_file.read())
        image = cv.imdecode(np.frombuffer(image_bytes.getbuffer(), np.uint8), cv.IMREAD_COLOR)
        
        # Convert the image to grayscale
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        
        # Detect faces using the cascade classifier
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            check_face = True
            FaceID = Generate.ID()  # Assuming you have the Generate.ID() function
            
            image_save = f".//{FaceID}.png"
            cv.imwrite(image_save, image[y:y+h, x:x+w])
            train_response = train([image_save, FaceID])  # Assuming you have the train() function
            if train_response:
                data = Users(names=names, email=email, userId=FaceID)  # Assuming you have the Users model
                db.session.add(data)  # Assuming you're using a database
                db.session.commit()
                print("User registered:", names)
            else:
                print("Training failed for user:", names)
        
        if check_face:
            return 'success'
        else:
            return 'No face detected'
    
    except cv.error as cv_err:
        return f"OpenCV Error: {str(cv_err)}"
    
    except Exception as e:
        return f"Unexpected Error: {str(e)}"


@app.route('/api/take_attendance')
def attendance_take():
    name = Recongonation.Rec()
    print(name)
    return 'hello'

@app.route("/api/enroll_faces/",methods=['POST', 'GET'])
def FaceEnroll():
    content=request.get_json();
    person_name=content['fname']
    name = EnrollFace.enroll(person_name)
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
