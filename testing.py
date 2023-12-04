import cv2

# Initialize the VideoCapture object with the webcam index (usually 0 for the first camera)
# If you have multiple cameras, you may need to change the index.
cap = cv2.VideoCapture(1)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Create a window to display the webcam feed
# cv2.namedWindow("Webcam Feed", cv2.WINDOW_NORMAL)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        print("Error: Could not read a frame from the camera.")
        break

    # Display the frame in the "Webcam Feed" window
    cv2.namedWindow('Webcam', cv2.WINDOW_NORMAL)

                # Resize the window to the desired dimensions
    cv2.resizeWindow('Webcam', 1000, 800)
    # cv2.setWindowProperty('QR Scanner', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Display the image in the resized window
    cv2.imshow('Webcam', frame)
    # cv2.imshow("Webcam Feed", frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
