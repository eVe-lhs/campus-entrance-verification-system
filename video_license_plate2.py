import numpy as np
from ultralytics import YOLO
import cv2
import pyautogui
import csv

# import license_plate_util
from license_plate_util import read_license_plate

screen_size = pyautogui.size()

results = {}

def verify(detectedNo):
	# Open a csv reader called DictReader
	with open('data.csv', encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		for rows in csvReader:
			
			# Assuming a column named 'No' to
			# be the primary key
			car_no = rows['car_no']
			if(car_no== detectedNo):
				return rows

# load model
license_plate_detector = YOLO('./models/best.pt')

def detect_plate():
# load video
    cap = cv2.VideoCapture('./videos/car_8.mp4')

    #load live camera
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # cap = cv2.VideoCapture(1)

    license_threshold = 0.6
    # read frames
    frame_nmr = -1

    # ret = True
    while True:
        frame_nmr += 1

        #get frame from videocapture
        ret, frame = cap.read()
        # Read from video file of video capture
        if ret:
            results[frame_nmr] = {}
                # detect license plates
            license_plates = license_plate_detector(frame)[0]
            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                if score > license_threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    # crop license plate
                    license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                    # process license plate
                    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                    _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 100, 255, cv2.THRESH_BINARY_INV)

                    # read license plate number
                    license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)
                    if license_plate_text is not None:
                        if(license_plate_text_score > 0.6):
                             cv2.putText(frame,license_plate_text,(int(x1)+5, int(y1)-10),cv2.FONT_HERSHEY_COMPLEX,1, (0, 255, 0), 1)
                             result = verify(license_plate_text)
                             if result:
                                  cv2.destroyAllWindows()
                                  return result
                                  
        else:
            cv2.destroyAllWindows()
            break
        
        # Display the frame in the "Webcam Feed" window
        cv2.namedWindow('Number plate detection', cv2.WINDOW_NORMAL)

                    # Resize the window to the desired dimensions
        cv2.resizeWindow('Number plate detection', 1000, 800)
        # cv2.setWindowProperty('QR Scanner', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Display the image in the resized window
        cv2.imshow('Number plate detection', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
