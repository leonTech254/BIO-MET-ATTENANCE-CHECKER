import cv2 as cv
from Models.model import Users
import sqlite3
from Models.db import db


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

        # Create a VideoCapture object
        capture = cv.VideoCapture(video_source)

        # Check if the video source is opened
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

            # Set the position of the text
            text_x = 10
            text_y = 30

            # Set the color of the text
            color = (255, 255, 0)
            for (x, y, w, h) in faces:
                # Draw a rectangle around the face
                cv.putText(colored, f"{name} {confidence}",
                           (x, y), font, font_scale, color, thickness)
            try:
                cv.rectangle(colored, (x, y), (x+w, y+h), (255, 0, 0), 2)
            except:
                pass

            if not ret:
                print("Error reading frame")
                break

            # Show the frame
            cv.imshow("Video", colored)

            # Wait for a key press
            key = cv.waitKey(1)
            if key == ord('q'):
                break

        # Release the VideoCapture object
        capture.release()

        # Close all windows
        cv.destroyAllWindows()

        return name
