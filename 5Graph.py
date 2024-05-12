import tkinter as tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import threading
import time


class SensorGraph:
    def __init__(self, master):
        self.master = master
        self.master.title("Sensor Graph")

        # Create a frame for the graph
        self.frame = tk.Frame(master, width=400, height=300)
        self.frame.pack()

        # Create a subplot for the graph
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Sensor Values")
        self.lines = [self.ax.plot([], [], label=f"Sensor {i + 1}")[0] for i in range(5)]

        # Move the legend to the bottom left
        self.ax.legend(loc='lower left')

        # Set the x-axis limits to show only the last 15 values
        self.ax.set_xlim(0, 15)

        # Create a canvas to display the graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

        # Start a thread to update the graph continuously
        self.running = True
        self.update_thread = threading.Thread(target=self.update_graph)
        self.update_thread.start()

    def update_graph(self):
        while self.running:
            # Generate random sensor values
            sensor_values = [random.uniform(0, 100) for _ in range(5)]

            # Append new data points to the graph
            for line, value in zip(self.lines, sensor_values):
                line.set_xdata(np.append(line.get_xdata(), len(line.get_xdata())))
                line.set_ydata(np.append(line.get_ydata(), value))

            # Update the x-axis limits to show only the last 15 values
            self.ax.set_xlim(max(0, len(self.lines[0].get_xdata()) - 10), len(self.lines[0].get_xdata()))

            # Update the graph
            self.ax.relim()
            self.ax.autoscale_view()
            self.canvas.draw()

            # Pause for a short interval
            time.sleep(0.2)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = SensorGraph(root)

    # Create a button to stop the graph updates
    stop_button = tk.Button(root, text="Stop", command=app.stop)
    stop_button.pack()

    root.mainloop()
