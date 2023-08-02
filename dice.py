import os
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Load dice images
dice_images = [Image.open(os.path.join("images", "dice", f"{i}spot.png")) for i in range(1, 7)]

class DiceApp:
    def __init__(self, root):
        self.root = root

        self.num_dice_var = tk.StringVar()
        self.num_dice_var.set("1")

        self.num_dice_label = ttk.Label(self.root, text="Number of Dice:")
        self.num_dice_label.pack()

        self.num_dice_combo = ttk.Combobox(self.root, textvariable=self.num_dice_var, values=["1", "2", "3", "4", "5", "6"])
        self.num_dice_combo.pack()

        self.roll_button = ttk.Button(self.root, text="Roll Dice", command=self.roll)
        self.roll_button.pack(pady=10)

        self.dice_canvas = tk.Canvas(self.root, width=500, height=150)  # Increased width to accommodate more dice
        self.dice_canvas.pack(pady=20)

    def roll(self):
        num_dice = self.num_dice_var.get()
        dice_images = roll_dice(int(num_dice))
        self.display_dice(dice_images)

    def display_dice(self, dice_images):
        self.dice_canvas.delete("all")
        x_offset = 10
        y_offset = 10
        self.dice_photo_images = []  # Clear existing PhotoImage objects
        for image in dice_images:
            photo = ImageTk.PhotoImage(image)
            self.dice_photo_images.append(photo)  # Store PhotoImage object
            self.dice_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=photo)
            x_offset += photo.width() + 10

        self.dice_canvas.update()



def roll_dice(num_dice):
    if not num_dice:
        return []

    try:
        dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        for value in dice_values:
            print(value)
        return [dice_images[value - 1] for value in dice_values]
    except ValueError:
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceApp(root)    
    root.mainloop()
