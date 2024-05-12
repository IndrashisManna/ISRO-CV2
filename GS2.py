import tkinter as tk
from PIL import Image, ImageTk
import pygame
from pygame.locals import *

import os


class SplitScreenApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Split Screen App")

        # Create frames for each section of the split screen
        self.frames = {}
        for i in range(2):
            for j in range(3):
                self.frames[(i, j)] = tk.Frame(master, bg="white", borderwidth=2, relief=tk.RIDGE)
                self.frames[(i, j)].grid(row=i, column=j, sticky="nsew")

        # Set row and column weights to make frames expand to fill the window
        for i in range(2):
            self.master.grid_rowconfigure(i, weight=1)
        for j in range(3):
            self.master.grid_columnconfigure(j, weight=1)

        # Display images and videos in each frame
        for position, frame in self.frames.items():
            if position == (0, 0):
                self.display_image(frame, "C:/Users/Indrashis/Pictures/Saved Pictures/1.jpg")  # Replace "path_to_image.jpg" with your image path
            elif position == (0, 1):
                self.display_image(frame, "C:/Users/Indrashis/Pictures/Saved Pictures/2.jpg")  # Replace "path_to_image.jpg" with your image path
            elif position == (1, 0):
                self.display_video(frame, "C:/Users/Indrashis/Videos/Edit/ISRO/vdo2.mp4")  # Replace "path_to_video.mp4" with your video path
            elif position == (1, 1):
                self.display_video(frame, "C:/Users/Indrashis/Videos/Edit/ISRO/vdo3.mp4")  # Replace "path_to_video.mp4" with your video path

    def display_image(self, frame, image_path):
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(frame, image=photo)
        label.image = photo
        label.pack(expand=True, fill="both")
        frame.update_idletasks()  # Ensure the frame dimensions are updated

    def display_video(self, frame, video_path):
        frame.update_idletasks()  # Ensure the frame dimensions are updated
        os.environ['SDL_WINDOWID'] = str(frame.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        pygame.display.set_caption("Video Player")
        screen = pygame.display.set_mode((frame.winfo_width(), frame.winfo_height()))
        clock = pygame.time.Clock()

        video = pygame.movie.Movie(video_path)
        video.set_display(screen, (0, 0, frame.winfo_width(), frame.winfo_height()))
        video.play()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    video.stop()
                    pygame.quit()

            pygame.display.flip()
            clock.tick(30)  # Decreased frame rate for smoother playback

        # Bind the close window event to the root window
        self.master.bind("<KeyPress>", self.close_window)

    def close_window(self, event):
        self.master.destroy()


def main():
    root = tk.Tk()
    app = SplitScreenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
