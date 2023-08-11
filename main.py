import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shuffle
import drawCard
import dice
import char
import journal

# Set the correct images directory path
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Create the main application window
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torch in the Dark 2.0")

        # Initialize journal_app attribute
        self.journal_window = None
        self.journal_app = None        

        # Create a frame for the top section (Shuffle Deck, Draw Card, Drawn Card)
        top_frame = ttk.Frame(self.root)
        top_frame.pack()

        self.shuffle_button = ttk.Button(top_frame, text="Shuffle Deck", command=self.shuffle_deck)
        self.shuffle_button.pack(side="left", padx=10, pady=10)        

        # Load a default card image (place this next to the "Draw Card" button)
        default_card_image_path = os.path.join("images", "cards", "default.png")
        if os.path.exists(default_card_image_path):
            default_card_image = Image.open(default_card_image_path)
            default_card_photo = ImageTk.PhotoImage(default_card_image)

            self.default_card_label = ttk.Label(top_frame, image=default_card_photo)
            self.default_card_label.photo = default_card_photo
            self.default_card_label.pack(side="left", padx=10, pady=10)

        # Create a frame for the roll dice section
        self.roll_dice_frame = ttk.LabelFrame(self.root, text="Roll Dice")
        self.roll_dice_frame.pack(padx=10, pady=10)

        self.roll_dice_app = dice.DiceApp(self.roll_dice_frame)  # Use dice.DiceApp

        # Create a frame for the buttons at the bottom
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side="bottom", pady=10)
        
        # Create an instance of the journal
        self.initialize_journal_app()  # Call the initialization method
        
        self.character_sheet_app = char.CharacterSheetApp(root)  # Create an instance of the character sheet app
        self.character_sheet_app.main_app = self  # Set the main_app attribute

        self.journal_app.text.pack(fill="both", expand=True, padx=10, pady=10)  # Place journal above the buttons

        self.character_button = ttk.Button(bottom_frame, text="Character", command=self.open_character_sheet)
        self.character_button.pack(side="left", padx=10)

        self.reference_button = ttk.Button(bottom_frame, text="Reference", command=self.show_reference)
        self.reference_button.pack(side="right", padx=10)

        # Create an instance of the journal
        self.open_journal()
        
        # Create the DrawCardApp instance
        self.draw_card_app = drawCard.DrawCardApp(top_frame, shuffle.draw_next_card, self.journal_app)
        self.draw_button = self.draw_card_app.draw_button
        self.draw_button.pack(side="left", padx=10, pady=10)

        self.card_label = self.draw_card_app.card_label

    def initialize_journal_app(self):
        if not self.journal_app:
            journal_window = tk.Toplevel(self.root)
            journal_window.title("Journal")
            self.journal_app = journal.JournalApp(journal_window)
    
    def initialize_draw_card_app(self):
        if not hasattr(self, 'draw_card_app'):
            self.draw_card_app = drawCard.DrawCardApp(self.root, self.journal_app)  # Pass 'root' and 'journal_app' as arguments

    def draw_card(self):
        self.initialize_draw_card_app()  # Initialize DrawCardApp if not already
        drawn_card = self.draw_card_app.draw_card()  # Call the draw_card method
        if drawn_card:
            print(f"Drawn Card: {drawn_card}")
            if self.journal_app:  # Check if journal_app exists before adding an entry
                self.journal_app.add_entry("Draw Card", f"Drawn Card: {drawn_card}", "red")

    def shuffle_deck(self):
        shuffle.shuffle_cards()  # Corrected call to shuffle_cards function
        print("Deck shuffled.")

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


    def open_journal(self):
        if self.journal_app:
            self.journal_app.show_journal_window()

    def open_character_sheet(self):
        character_sheet_window = tk.Toplevel(self.root)
        character_sheet_window.title("Character Sheet")
        self.character_sheet_app = char.CharacterSheetApp(character_sheet_window)
        self.character_sheet_app.main_app = self  # Set the main_app attribute



if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
