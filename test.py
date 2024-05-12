import tkinter as tk
from PIL import ImageTk, Image
import cv2

class VideoPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Video Player")

        # Load videos
        self.video1_path =  r'C:\Users\Indrashis\Videos\Edit\ISRO\vdo3.mp4'
        self.video2_path =  r'C:\Users\Indrashis\Videos\Edit\ISRO\vdo2.mp4'

        # Create frames for each video
        self.frame1 = tk.Frame(master, width=450, height=300)
        self.frame1.grid(row=0, column=0)

        self.frame2 = tk.Frame(master, width=450, height=300)
        self.frame2.grid(row=0, column=1)

        # Display videos
        self.display_video(self.video1_path, self.frame1)
        self.display_video(self.video2_path, self.frame2)

    def display_video(self, video_path, frame):
        # Open video file
        cap = cv2.VideoCapture(video_path)

        # Read the first frame
        ret, frame_img = cap.read()

        # Convert frame to RGB format
        frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)

        # Resize frame to fit the frame size
        frame_img = cv2.resize(frame_img, (450, 300))

        # Convert frame to ImageTk format
        frame_img = Image.fromarray(frame_img)
        frame_img = ImageTk.PhotoImage(frame_img)

        # Create label to display the video
        label = tk.Label(frame, image=frame_img)
        label.image = frame_img  # Keep a reference to avoid garbage collection
        label.pack()

        # Update the display periodically
        def update_video():
            nonlocal frame_img

            ret, frame_img = cap.read()
            if ret:
                frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
                frame_img = cv2.resize(frame_img, (450, 300))
                frame_img = Image.fromarray(frame_img)
                frame_img = ImageTk.PhotoImage(frame_img)
                label.configure(image=frame_img)
                label.image = frame_img
                label.after(10, update_video)  # Update every 10 milliseconds
            else:
                cap.release()

        # Start updating the video
        update_video()


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayer(root)
    root.mainloop()
