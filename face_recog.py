import face_recognition
import os, sys
import cv2
import numpy as np
import math
import time
from threading import Thread
from multiprocessing import Process
import csv

def verifyFace(face_image):
	# Open a csv reader called DictReader
	with open('data.csv', encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for rows in csvReader:
			
			# Assuming a column named 'No' to
			# be the primary key
			face_img = rows['face_image']
			if(face_img== face_image):
				return rows

# Helper
class WebcamStream:
    # initialization method
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for main camera

        # opening video capture stream
        self.vcap = cv2.VideoCapture(self.stream_id, cv2.CAP_DSHOW)
        # self.vcap = cv2.VideoCapture(self.stream_id)

        # self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.vcap.get(5))  # hardware fps
        print("FPS of input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        # self.stopped is initialized to False
        self.stopped = True
        # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()

    # method passed to thread to read next available frame
    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.vcap.release()

    # method to return latest read frame
    def read(self):
        return self.frame

    # method to stop reading frames
    def stop(self):
        self.stopped = True


def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True
    result = None


    def __init__(self):
        self.encode_faces()
        self.t = Thread(target=self.run_recognition, args=())
        self.t.daemon = True  # daemon threads run in background

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)



    def run_recognition(self):
        video_capture = WebcamStream(stream_id=0)
        video_capture.start()
        if video_capture.stopped is True:
            sys.exit('Video source not found...')
        pTime = 0
        while True:
            frame = video_capture.read()
            frame = cv2.flip(frame, 1)
            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.16, fy=0.16)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                # rgb_small_frame = small_frame[:, :, ::-1]
                rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.4)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        video_capture.stop()
                        cv2.destroyAllWindows()
                        return verifyFace(name)
                    self.face_names.append(name)
                        

            self.process_current_frame = not self.process_current_frame
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 6.25
                right *= 6.25
                bottom *= 6.25
                left *= 6.25

                # Create the frame with the name
                cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 0, 255), 2)
                cv2.rectangle(frame, (int(left), int(bottom) - 35), (int(right), int(bottom)), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (int(left) + 6, int(bottom) - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            # Display the resulting image
            time.sleep(0.03)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                        (255, 0, 255), 3)

            # Display the results
            cv2.namedWindow('Face Detection', cv2.WINDOW_NORMAL)

                # Resize the window to the desired dimensions
            cv2.resizeWindow('Face Detection', 1000, 800)
            # cv2.setWindowProperty('Face Detection', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                # Display the image in the resized window
            cv2.imshow('Face Detection', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.stop()
        cv2.destroyAllWindows()


# if __name__ == '__main__':
#     fr = FaceRecognition()
#     fr.run_recognition()
#     print(fr.result)
