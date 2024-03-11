import cv2
import numpy as np

# Global variables to store object coordinates and dimensions
x, y, w, h = 0, 0, 0, 0

def detect_cars(frame, net, classes, layer_names):
    global x, y, w, h  # Declare them as global to modify their values

    # Create a blob from the frame
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)

    # Set the blob as input to the neural network
    net.setInput(blob)

    # Forward pass to get the output layer predictions
    layer_outputs = net.forward(layer_names)

    # Initialize lists for bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    # Iterate over each output layer
    for output in layer_outputs:
        # Iterate over each detection in the output
        for detection in output:
            # Extract the class ID and confidence of the current detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # Filter out weak detections by ensuring the confidence is above a threshold
            if confidence > 0.5:
                # Scale the bounding box coordinates to the frame size
                box = detection[0:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (centerX, centerY, width, height) = box.astype("int")

                # Calculate the top-left corner of the bounding box
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                w = int(width)
                h = int(height)

                # Update the lists of bounding boxes, confidences, and class IDs
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply non-maximum suppression to suppress weak, overlapping bounding boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw the bounding boxes and labels on the frame
    for i in indices.flatten():
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])
        color = (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(classes[class_ids[i]], confidences[i])
        cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame

def main():
    global x, y, w, h  # Declare them as global to access their values

    # Load the pre-trained YOLO model
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Load the COCO class labels
    with open("coco.names", "r") as f:
        classes = f.read().strip().split("\n")

    # Get the output layer names
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't capture frame.")
            break

        # Detect cars in the frame using YOLO
        detected_frame = detect_cars(frame, net, classes, output_layers)

        # Display the frame with car detections
        cv2.imshow('Car Detection', detected_frame)

        # Print the coordinates and dimensions in the format (x, y, w, h)
        print(f"Coordinates and Dimensions: ({x}, {y}, {w}, {h})")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
