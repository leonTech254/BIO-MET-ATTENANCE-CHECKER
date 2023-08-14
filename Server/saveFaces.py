import cv2
import os

# Create a directory to store captured images
output_dir = 'captured_faces'
os.makedirs(output_dir, exist_ok=True)

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Set the number of face images to capture
num_faces_to_capture = 50
current_face_count = 0

# Initialize the camera
cap = cv2.VideoCapture(0)

while current_face_count < num_faces_to_capture:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        # Save the captured face image
        face_filename = os.path.join(output_dir, f'face_{current_face_count}.jpg')
        cv2.imwrite(face_filename, face)

        current_face_count += 1

        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Capture Faces', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()

print(f"{current_face_count} face(s) captured and saved successfully.")
