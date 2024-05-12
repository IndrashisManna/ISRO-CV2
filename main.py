import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


class RoverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Rover Display")

        # Create frames for each section of the GUI
        self.frames = {}
        for i in range(3):
            for j in range(2):
                self.frames[(i, j)] = tk.Frame(master, width=300, height=200, borderwidth=2, relief=tk.RIDGE)
                self.frames[(i, j)].grid(row=i, column=j, padx=5, pady=5)

        # Display video from cam 1 (Screen 0,0)
        self.display_video("cam1.jpg", (0, 0))

        # Display video from cam 2 (Screen 0,1)
        self.display_video("cam2.jpg", (0, 1))

        # Display values of 5 movement sensors (Screen 1,0)
        self.display_sensor_values((1, 0))

        # Display path traversal animation (Screen 1,1)
        self.display_path_animation((1, 1))

        # Display gyroscopic value by animation (Screen 2,0)
        self.display_gyro_animation((2, 0))

        # Display continuous graph of signal strength (Screen 2,1)
        self.display_signal_graph((2, 1))

    def display_video(self, image_path, position):
        img = ImageTk.PhotoImage(Image.open(image_path).resize((150, 100), Image.ANTIALIAS))
        label = tk.Label(self.frames[position], image=img)
        label.image = img  # Keep a reference to avoid garbage collection
        label.pack()

    def display_sensor_values(self, position):
        sensor_values = ["Sensor 1: 50", "Sensor 2: 40", "Sensor 3: 60", "Sensor 4: 55", "Sensor 5: 45"]
        text = "\n".join(sensor_values)
        label = tk.Label(self.frames[position], text=text)
        label.pack()

    def display_path_animation(self, position):
        # Placeholder for path traversal animation
        canvas = tk.Canvas(self.frames[position], width=150, height=100, bg="white")
        canvas.create_line(10, 10, 50, 50, fill="blue", width=2)
        canvas.pack()

    def display_gyro_animation(self, position):
        # Placeholder for gyroscopic animation
        canvas = tk.Canvas(self.frames[position], width=150, height=100, bg="white")
        canvas.create_oval(10, 10, 50, 50, fill="green")
        canvas.pack()

    def display_signal_graph(self, position):
        # Placeholder for signal strength graph
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)

        canvas = FigureCanvasTkAgg(fig, master=self.frames[position])
        canvas.draw()
        canvas.get_tk_widget().pack()


root = tk.Tk()
app = RoverGUI(root)
root.mainloop()
