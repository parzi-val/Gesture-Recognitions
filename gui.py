from PIL import Image, ImageTk
import tkinter as tk
from time import sleep
from threading import Thread

class ImageZoomApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Zoom Application")

        # Load your initial image
        self.pil_image = Image.open("cat.png")
        self.image = ImageTk.PhotoImage(self.pil_image)
        
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

        self.zoom_factor = 1.0

    def zoom_image(self, zoom_in=True):
        # Get the current image size
        current_width, current_height = self.pil_image.size

        # Determine the scaling factor (zoom in or out)
        scale = 1.1 if zoom_in else 0.9

        # Calculate the new width and height
        new_width = int(current_width * scale)
        new_height = int(current_height * scale)

        # Resize the image using PIL
        self.pil_image = self.pil_image.resize((new_width, new_height))

        # Convert the PIL image back to a PhotoImage
        self.image = ImageTk.PhotoImage(self.pil_image)

        # Update the image on the canvas
        self.canvas.itemconfig(self.image_item, image=self.image)

if __name__ == "__main__":    
    root = tk.Tk()
    app = ImageZoomApp(root)
    root.mainloop()

