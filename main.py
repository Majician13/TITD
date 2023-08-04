import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shuffle
import drawCard
import dice
import char  # Import the char module

# Set the correct images directory path
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Create the main application window
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torch in the Dark 2.0")

        # Create a frame for the top section (Shuffle Deck, Draw Card, Drawn Card)
        top_frame = ttk.Frame(self.root)
        top_frame.pack()

        self.shuffle_button = ttk.Button(top_frame, text="Shuffle Deck", command=self.shuffle_deck)
        self.shuffle_button.pack(side="left", padx=10, pady=10)

        self.draw_card_app = drawCard.DrawCardApp(top_frame)  # Create DrawCardApp instance

        self.draw_button = ttk.Button(top_frame, text="Draw Card", command=self.draw_card)
        self.draw_button.pack(side="left", padx=10, pady=10)

        self.card_label = ttk.Label(top_frame, text="", font=("Helvetica", 16))
        self.card_label.pack(side="left", padx=10, pady=10)

        # Create a frame for the roll dice section
        self.roll_dice_frame = ttk.LabelFrame(self.root, text="Roll Dice")
        self.roll_dice_frame.pack(padx=10, pady=10)

        self.roll_dice_app = dice.DiceApp(self.roll_dice_frame)  # Use dice.DiceApp

        # Create a frame for the buttons at the bottom
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side="bottom", pady=10)

        self.character_button = ttk.Button(bottom_frame, text="Character", command=self.open_character_sheet)
        self.character_button.pack(side="left", padx=10)

        self.reference_button = ttk.Button(bottom_frame, text="Reference", command=self.show_reference)
        self.reference_button.pack(side="right", padx=10)

    def open_character_sheet(self):
        character_window = tk.Toplevel(self.root)
        character_window.title("Character Sheet")
        character_app = char.CharacterSheetApp(character_window)

    def draw_card(self):
        """Draw a card and display it on the card_label."""
        try:
            self.draw_card_app.draw_card(self.card_label)
        except IndexError:
            self.card_label.config(text="Error: Card deck is empty", image=None)

    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        try:
            shuffle.shuffle_cards()
            print("Deck shuffled.")
        except Exception as e:
            print("Error shuffling cards:", e)

    def show_reference(self):
        """Display a pop-up window with the reference image."""
        reference_window = tk.Toplevel(self.root)
        reference_window.title("Reference Image")
        
        screen_width = reference_window.winfo_screenwidth()
        screen_height = reference_window.winfo_screenheight()
        initial_width = int(screen_width * 0.5)
        initial_height = int(screen_height * 0.5)
        
        reference_window.geometry(f"{initial_width}x{initial_height}")
        
        try:
            reference_image = Image.open(os.path.join(IMAGE_DIR, "TITDReference.png"))
            reference_label = ttk.Label(reference_window)
            reference_label.pack(fill="both", expand=True)
            
            def resize_image(event):
                new_width = event.width - 10
                new_height = event.height - 10
                resized_image = reference_image.resize((new_width, new_height), Image.ANTIALIAS)
                new_reference_image = ImageTk.PhotoImage(resized_image)
                reference_label.config(image=new_reference_image)
                reference_label.image = new_reference_image
                
            reference_window.bind("<Configure>", resize_image)
            resize_image(reference_label.winfo_geometry())
        except Exception as e:
            print("Error displaying reference image:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
