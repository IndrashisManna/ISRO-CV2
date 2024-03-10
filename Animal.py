import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
def detect_red_cylinder(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Convert to grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use HoughCircles to detect circles
    circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=50, param2=30, minRadius=10, maxRadius=100)

    # Draw detected circles with confidence level
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            radius = i[2]
            confidence = calculate_confidence(frame, center, radius)
            if confidence > 0.5:
                cv2.circle(frame, center, radius, (0, 255, 0), 2)
                cv2.putText(frame, f'Red Cylinder ({confidence:.2f})', (i[0]-50, i[1]-20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

def calculate_confidence(frame, center, radius):

    return np.random.uniform(0, 1)  # Random confidence for demonstration

def main():
    path = r'C:\Users\Indrashis\Videos\Edit\Animal.mp4'
    cap = cv2.VideoCapture(path)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            break

        detected_frame = detect_red_cylinder(frame)
        cv2.imshow('Red Cylinder Detection', detected_frame)

        if cv2.waitKey(24) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
