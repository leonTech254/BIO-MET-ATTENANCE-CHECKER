import cv2
import os
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
face_count = 0
face_limit = 50
output_folder = 'captured_faces2'
os.makedirs(output_folder, exist_ok=True)
while True:
    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x,y,w,h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_filename = os.path.join(output_folder, f'face_{face_count}.jpg')
        cv2.imwrite(face_filename, face_img)
        face_count += 1
        
    cv2.imshow('frame', frame)
    
    if face_count >= face_limit:
        break

cap.release() 
cv2.destroyAllWindows()

print('Faces captured and saved successfully!')
