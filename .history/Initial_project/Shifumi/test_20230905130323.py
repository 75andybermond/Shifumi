import cv2

# Open the default camera
cap = cv2.VideoCapture(2)

while True:
    # Capture a frame
    ret, frame = cap.read()

    # Check if the frame is valid
    if not ret:
        break

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()