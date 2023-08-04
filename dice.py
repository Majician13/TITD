import os
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class DiceApp:
    def __init__(self, root):
        self.root = root

        # Load dice images
        self.dice_images = [Image.open(os.path.join("images", "dice", f"{i}spot.png")) for i in range(1, 7)]

        # Create dice labels based on the maximum possible number of dice (6)
        self.dice_labels = []
        for _ in range(6):
            dice_label = ttk.Label(self.root)
            dice_label.pack(side=tk.LEFT, padx=5)
            self.dice_labels.append(dice_label)  # Add the dice label to the list

        self.num_dice_var = tk.StringVar()
        self.num_dice_var.set("1")

        self.zero_negative_var = tk.IntVar()  # Variable for Zero/Negative Dice checkbox
        self.zero_negative_check = ttk.Checkbutton(self.root, text="Zero/Negative Dice", variable=self.zero_negative_var)
        self.zero_negative_check.pack()

        self.num_dice_label = ttk.Label(self.root, text="Number of Dice:")
        self.num_dice_label.pack()

        self.num_dice_combo = ttk.Combobox(self.root, textvariable=self.num_dice_var, values=["1", "2", "3", "4", "5", "6"])
        self.num_dice_combo.pack()

        self.roll_button = ttk.Button(self.root, text="Roll Dice", command=self.roll)
        self.roll_button.pack(pady=10)

        self.result_label = ttk.Label(self.root, text="")
        self.result_label.pack()

    def roll(self):
        num_dice = int(self.num_dice_var.get())  # Convert the string to an integer
        zero_negative = self.zero_negative_var.get()  # Get the value of the Zero/Negative Dice checkbox
        print("Zero/Negative Dice:", zero_negative)  # Debugging print
        dice_values = roll_dice(num_dice)
        print("Rolled Dice Values:", dice_values)  # Debugging print
        self.display_dice(dice_values)

    def display_dice(self, dice_values):
        # Clear previous text
        self.result_label.config(text="")

        # Clear previous dice images and references
        for dice_label in self.dice_labels:
            dice_label.config(image=None)
            dice_label.image = None

        # Display dice images
        for i, value in enumerate(dice_values):
            if 1 <= value <= 6:
                dice_label = self.dice_labels[i]
                dice_image = ImageTk.PhotoImage(self.dice_images[value - 1])
                dice_label.config(image=dice_image)
                dice_label.image = dice_image  # Save a reference to prevent garbage collection

        # Hide unused dice images
        for i in range(len(dice_values), len(self.dice_labels)):
            dice_label = self.dice_labels[i]
            dice_label.config(image=None)
            dice_label.image = None
            
        # Display result text
        zero_negative = self.zero_negative_var.get()
        dice_value = dice_values[0]  # Assuming you want to display the text based on the first dice value
        result_text = self.get_result_text(dice_value, dice_values, zero_negative)
        self.result_label.config(text=result_text)
        print("Result Text:", result_text)  # Debugging print

    def get_result_text(self, dice_value, dice_values, zero_negative):
        if zero_negative:
            if min(dice_values) <= 3:
                return "Fail. Mark 1 XP. Consequence. Risk It!"
            elif min(dice_values) in (4, 5):
                return "Success with Consequence"
            elif min(dice_values) == 6:
                return "Success"
            else:
                return ""
        else:
            if max(dice_values) == 6:
                if dice_values.count(6) > 1:
                    return "Critical Success, Clear 1 Stress or Corruption"
                else:
                    return "Success"
            elif max(dice_values) in (4, 5):
                return "Success with Consequence"
            elif max(dice_values) in (1, 2, 3):
                return "Fail. Mark 1 XP. Consequence. Risk It!"
            else:
                return ""



# Rest of the code
def roll_dice(num_dice):
    dice_values = [random.randint(1, 6) for _ in range(num_dice)]  # Adjust range to 0-5
    return dice_values

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceApp(root)
    root.mainloop()
