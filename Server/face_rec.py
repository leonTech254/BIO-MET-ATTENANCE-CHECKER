import cv2 as cv
from Models.model import Users
import sqlite3
from Models.db import db
import os


class store:
    all_user = False


def check_name(id):
    print(id)
    try:
        user = Users.query.filter_by(UserId=str(id)).first()
        user.present = 'present'
        db.session.commit()
        return store.all_user[str(id)]
    except:
        print(store.all_user)
        return "checking...."


class Recongonation:
    def Rec():
        users = Users.query.all()
        user_dict = {}
        for user in users:
            user_dict[user.UserId] = user.Names
        store.all_user = user_dict

        face_recongonation = cv.face.LBPHFaceRecognizer_create()
        face_recongonation.read("./model.yml")
        face_cascade = cv.CascadeClassifier(
            "./OpencvCascades/haarcascade_frontalface_default.xml")
        video_source = 0

        capture = cv.VideoCapture(video_source)

        if not capture.isOpened():
            print("Error opening video source")

        capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

        while True:
            ret, frame = capture.read()
            colored = frame
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(frame, 1.3, 5)

            label, confidence = face_recongonation.predict(frame)
            check_name(label)
            name = check_name(label)

            font = cv.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2

            text_x = 10
            text_y = 30

            color = (255, 255, 0)
            for (x, y, w, h) in faces:
                cv.putText(colored, f"{name} {confidence}",
                           (x, y), font, font_scale, color, thickness)
            try:
                cv.rectangle(colored, (x, y), (x+w, y+h), (255, 0, 0), 2)
            except:
                pass

            if not ret:
                print("Error reading frame")
                break

            cv.imshow("Video", colored)

            key = cv.waitKey(1)
            if key == ord('q'):
                break

        capture.release()

        cv.destroyAllWindows()

        return name



class EnrollFace:
    def enroll(personname):
        output_dir = personname
        os.makedirs(output_dir, exist_ok=True)

        face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')

        num_faces_to_capture = 50
        current_face_count = 0

        cap = cv.VideoCapture(0)

        while current_face_count < num_faces_to_capture:
            ret, frame = cap.read()

            if not ret:
                break

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]

                face_filename = os.path.join(output_dir, f'face_{current_face_count}.jpg')
                cv.imwrite(face_filename, face)

                current_face_count += 1

                cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv.imshow('Capture Faces', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv.destroyAllWindows()
        return "saved"

        print(f"{current_face_count} face(s) captured and saved successfully.")