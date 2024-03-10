import cv2

def play_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is successfully opened
    if not cap.isOpened():
        print("Error: Could not open the video.")
        return

    # Read and display frames until the video ends
    while True:
        ret, frame = cap.read()

        # Check if the frame is successfully read
        if not ret:
            print("Video playback completed.")
            break

        # Display the frame
        cv2.imshow('Video', frame)

        # Wait for a short duration and check for user input to exit
        #if cv2.waitKey(24) & 0xFF == ord('q'):
        #    break
        cv2.waitKey(15)
    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.waitKey(1)
    cv2.destroyAllWindows()

# Path to the video file
video_path = r'C:\Users\Indrashis\Videos\Edit\Khosla Project.mp4'

# Call the function to play the video
play_video(video_path)


