import tkinter as tk
import colorsys

class ContinuousColorSquareApp:
    def __init__(self, master):
        self.master = master
        self.master.title("COLOUR SCHEME")

        self.side_length = 400
        self.num_colors = 100

        self.canvas = tk.Canvas(self.master, width=self.side_length, height=self.side_length, bg="black")
        self.canvas.pack()

        self.label = tk.Label(self.master, text="", font=("Helvetica", 12), fg="white", bg="black")
        self.label.pack(pady=10)

        self.draw_continuous_square()

        # Bind the motion event to the mouse_motion method
        self.canvas.bind("<Motion>", self.mouse_motion)

    def draw_continuous_square(self):
        block_size = self.side_length // self.num_colors

        for i in range(self.num_colors):
            for j in range(self.num_colors):
                hue = (i + j) / (2 * self.num_colors)  # Hue values range from 0 to 1
                rgb_color = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(hue, 1.0, 1.0))
                color = "#{:02X}{:02X}{:02X}".format(*rgb_color)
                self.canvas.create_rectangle(i * block_size, j * block_size, (i + 1) * block_size,
                                             (j + 1) * block_size, fill=color, outline=color)

    def mouse_motion(self, event):
        # Calculate the cell coordinates based on the mouse position
        cell_size = self.side_length // self.num_colors
        cell_x = event.x // cell_size
        cell_y = event.y // cell_size

        # Update the label text with the current cell coordinates
        self.label.config(text=f"X, Y = {cell_x}, {cell_y}")

def main():
    root = tk.Tk()
    app = ContinuousColorSquareApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()