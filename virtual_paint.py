import cv2
import numpy as np

# Initialize the drawing variables
drawing = False  # True if the mouse is pressed
last_x, last_y = None, None
color = (255, 0, 0)  # Blue color in BGR format
thickness = 5  # Thickness of the brush

# Callback function to draw on the canvas
def draw_circle(event, x, y, flags, param):
    global last_x, last_y, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(canvas, (last_x, last_y), (x, y), color, thickness)
            last_x, last_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(canvas, (last_x, last_y), (x, y), color, thickness)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Read the first frame to get the dimensions
ret, frame = cap.read()
if not ret:
    print("Error: Could not read frame from camera.")
    cap.release()
    exit()

# Create a black canvas with the same size as the frame
canvas = np.zeros(frame.shape, np.uint8)

# Create a window and bind the mouse callback function
cv2.namedWindow('Air Canvas')
cv2.setMouseCallback('Air Canvas', draw_circle)

# Start the drawing loop
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from camera.")
        break

    # Flip the frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Combine the canvas with the current frame
    combined = cv2.add(frame, canvas)

    # Display the resulting frame
    cv2.imshow('Air Canvas', combined)

    # Break the loop if the user presses 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the windows
cap.release()
cv2.destroyAllWindows()
