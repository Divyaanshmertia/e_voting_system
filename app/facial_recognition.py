import face_recognition
import io
from google.cloud import storage
import numpy as np
import cv2
import math

class FaceRecognition:
    def __init__(self, username):
        self.client = storage.Client()
        self.bucket_name = 'facerepo'  # Ensure this matches your actual bucket name
        self.bucket = self.client.bucket(self.bucket_name)
        self.username = username
        self.known_face_encodings = []
        self.known_face_names = []
        self.encode_faces()

    def encode_faces(self):
        user_folder = f"{self.username}/"  # Path to user's folder
        blobs = self.bucket.list_blobs(prefix=user_folder)
        for blob in blobs:
            if not blob.name.lower().endswith(('.jpg', '.png')):
                continue
            blob_bytes = blob.download_as_bytes()
            image = face_recognition.load_image_file(io.BytesIO(blob_bytes))
            face_encodings = face_recognition.face_encodings(image)
            if face_encodings:
                self.known_face_encodings.append(face_encodings[0])
                # Using the image name as a "name" for the face, adjust as needed
                self.known_face_names.append(blob.name.split('/')[-1])

    def face_confidence(self, face_distance, face_match_threshold=0.6):
        if face_distance > face_match_threshold:
            return "Unknown"
        else:
            range = (1.0 - face_match_threshold)
            linear_value = (1.0 - face_distance) / (range * 2.0)
            value = (linear_value + ((1.0 - linear_value) * math.pow((linear_value - 0.5) * 2, 0.2))) * 100
            return str(round(value, 2)) + '%'

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            print("Video Source not found .....")
            return

        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"
                confidence = "Unknown"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
                    confidence = self.face_confidence(face_distances[best_match_index])

                face_names.append(f'{name} ({confidence})')

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

            cv2.imshow('Face Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    username = 'A002'  # This should be dynamically determined
    fr = FaceRecognition(username)
    fr.run_recognition()
