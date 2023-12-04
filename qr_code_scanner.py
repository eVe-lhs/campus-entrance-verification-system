import cv2
import pyzbar.pyzbar as pyzbar
import re
import csv

# Create a flag to control the QR code scanning loop
scanning = False

# Function to handle the QR code scanning
def scan_qr_code():
    global scanning
    scanning = True
    # Create a VideoCapture object to capture video from the camera

    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

    try:
        while scanning:
            # Create a new connection and cursor within the scanning loop
                ret, frame = cap.read()
                frame = cv2.flip(frame, 1)

                # Find and decode QR codes in the frame
                decoded_objects = pyzbar.decode(frame)
                result = ''
                info = ''

                for obj in decoded_objects:
                    # Extract the data from the QR code
                    qr_data = obj.data.decode("utf-8")
                    qr_data = qr_data.replace('-','')
                    result = re.sub(r'[a-z]*', '', qr_data)

                with open('data.csv', encoding='utf-8') as csvf:
                    csvReader = csv.DictReader(csvf)
                    id = 0
                    for rows in csvReader:
                        id += 1
                        reg_no = rows['reg.no']
                        if(result and result == reg_no):
                            cv2.destroyAllWindows()
                            return rows
                        elif (result and result != reg_no):
                            cv2.putText(frame,'Unknown Identity',(10,40) , cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255) , 2)
                        else:
                            cv2.putText(frame,'No QR code detected yet',(10,40) , cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255) , 2)
                # Display the QR code data
                # Create a named window
                cv2.namedWindow('QR Scanner', cv2.WINDOW_NORMAL)

                # Resize the window to the desired dimensions
                cv2.resizeWindow('QR Scanner', 1000, 800)
                # cv2.setWindowProperty('QR Scanner', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                # Display the image in the resized window
                cv2.imshow('QR Scanner', frame)
                # Check for key press events
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

    except KeyboardInterrupt:
        # Handle the Keyboard Interrupt gracefully
        print("QR code scanning interrupted")

    finally:
        # Release the VideoCapture
        cap.release()

# if __name__ == "__main__":
#     scan_qr_code()

