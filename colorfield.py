import tkinter as tk
import colorsys
import sounddevice as sd
import numpy as np
import threading

class ContinuousColorSquareApp:
    def __init__(self, master):
        self.master = master
        self.master.title("COLOUR SCHEME")

        self.side_length = 400
        self.num_colors = 100
        self.color_array = []

        self.canvas = tk.Canvas(self.master, width=self.side_length, height=self.side_length, bg="black")
        self.canvas.pack()

        self.label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="white", bg="black")
        self.label.pack(pady=10)

        self.draw_continuous_square()

        # Bind events to canvas
        self.canvas.bind("<Motion>", self.mouse_motion)
        self.canvas.bind("<Enter>", self.mouse_enter)
        self.canvas.bind("<Leave>", self.mouse_leave)

        # Initialize audio variables
        self.current_frequencies = (440, 440, 440)

        # Create a thread for continuous audio playback
        self.audio_thread = threading.Thread(target=self.play_continuous_audio)
        self.audio_thread.daemon = True  # Allow the thread to be terminated when the main program exits
        self.audio_thread.start()

    def draw_continuous_square(self):
        block_size = self.side_length // self.num_colors

        for i in range(self.num_colors):
            row = []
            for j in range(self.num_colors):
                hue = (i + j) / (2 * self.num_colors)  # Hue values range from 0 to 1
                rgb_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0))
                color = "#{:02X}{:02X}{:02X}".format(*rgb_color)
                self.canvas.create_rectangle(i * block_size, j * block_size, (i + 1) * block_size,
                                             (j + 1) * block_size, fill=color, outline=color)
                row.append(rgb_color)
            self.color_array.append(row)

    def mouse_motion(self, event):
        # Calculate the cell coordinates based on the mouse position
        cell_size = self.side_length // self.num_colors
        cell_x = event.x // cell_size
        cell_y = event.y // cell_size
        frequencies = self.colour_to_frequencies(cell_x, cell_y)

        # Check if the frequencies have changed
        if frequencies != self.current_frequencies:
            # Update the current frequencies
            self.current_frequencies = frequencies

        # Update the label text with the current cell coordinates
        self.label.config(text=f"({frequencies})")

    def mouse_enter(self, event):
        # Do something when the mouse enters the canvas
        pass

    def mouse_leave(self, event):
        # Do something when the mouse leaves the canvas
        pass

    def colour_to_frequencies(self, x, y):
        """ (R 0-255, G, B) -> (freq1, freq2, freq3)
        440 <= freq <= 880
        """
        red_value = self.color_array[y][x][0]
        green_value = self.color_array[y][x][1]
        blue_value = self.color_array[y][x][2]
        return ((1 + red_value / 255) * 440, (1 + green_value / 255) * 440, (1 + blue_value / 255) * 440)

    def play_continuous_audio(self):
        while True:
            chord = self.generate_chord(0.5, self.current_frequencies, sample_rate=44100)
            sd.play(chord, 44100)
            sd.wait()

    def generate_chord(self, duration, frequencies, sample_rate):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        waves = [np.sin(2 * np.pi * f * t) * 0.1 for f in frequencies]
        chord = np.sum(waves, axis=0)
        return chord

def main():
    root = tk.Tk()
    app = ContinuousColorSquareApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()