import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shuffle
import drawCard
import dice
from char import CharacterSheetApp
from journal import JournalApp  # Import only the JournalApp class

# Set the correct images directory path
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")

# Create the main application window
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Torch in the Dark 2.0")
        
        # Create a frame for the top section (Shuffle Deck, Draw Card, Drawn Card)
        top_frame = ttk.Frame(self.root)
        top_frame.pack(side="left", padx=10, pady=10)

        self.shuffle_button = ttk.Button(top_frame, text="Shuffle Deck", command=self.shuffle_deck)
        self.shuffle_button.pack(side="top", padx=10, pady=10)

        # Load a default card image (place this next to the "Draw Card" button)
        default_card_image_path = os.path.join("images", "cards", "default.png")
        if os.path.exists(default_card_image_path):
            default_card_image = Image.open(default_card_image_path)
            default_card_photo = ImageTk.PhotoImage(default_card_image)

            self.default_card_label = ttk.Label(top_frame, image=default_card_photo)
            self.default_card_label.photo = default_card_photo
            self.default_card_label.pack(side="left", padx=10, pady=10)

        # Create frames for left and right sections
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side="left", padx=10, pady=10, fill="both")

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side="right", padx=10, pady=10, fill="both")

        # Create an instance of the character sheet app and pass the right_frame as a parent
        self.character_sheet_app = CharacterSheetApp(right_frame, self)  # Use the imported CharacterSheetApp class

        # Create a frame for the roll dice section
        self.roll_dice_frame = ttk.LabelFrame(self.root, text="Roll Dice")
        self.roll_dice_frame.pack(side="left", padx=10, pady=10)

        # Create the JournalApp instance for the separate journal window
        journal_window = tk.Toplevel(root)
        journal_window.title("Journal")
        self.journal_app = JournalApp(journal_window)

        # Create the DiceApp instance and connect it to the frame
        self.roll_dice_app = dice.DiceApp(self.roll_dice_frame, self.journal_app)


        # Create a frame for the buttons at the bottom
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(side="bottom", pady=10)

        # Save Button
        save_button = ttk.Button(bottom_frame, text="Save", command=self.save_data)
        save_button.pack(side="left", padx=10, pady=10)

        # Load Button
        load_button = ttk.Button(bottom_frame, text="Load", command=self.load_data)
        load_button.pack(side="left", padx=10, pady=10)

        # Journal Button
        journal_button = ttk.Button(bottom_frame, text="Journal", command=self.open_journal)
        journal_button.pack(side="left", padx=10, pady=10)

        # Reference Button
        reference_button = ttk.Button(bottom_frame, text="Reference", command=self.show_reference)
        reference_button.pack(side="left", padx=10, pady=10)

        # Create the DrawCardApp instance
        self.draw_card_app = drawCard.DrawCardApp(top_frame, shuffle.draw_next_card, self.journal_app)
        self.draw_button = self.draw_card_app.draw_button
        self.draw_button.pack(side="left", padx=10, pady=10)

    

    def save_data(self):
        # Get character sheet data (assuming you have a method to retrieve character sheet data)
        character_data = self.character_sheet_app.get_character_data()  # Use the method you define in CharacterSheetApp

        # Save data to data_manager
        data_manager.save_data(character_data, self.journal_app.get_journal_text())

        # Save data to a file
        data_manager.save_to_file("saved_data.json")

    def load_data(self):
        # Load data from the file
        data_manager.load_from_file("saved_data.json")

        # # Set character sheet data (assuming you have a method to set character sheet data)
        # self.character_sheet_app.set_character_data(data_manager.character_data)

        # Set journal text
        self.journal_app.set_journal_text(data_manager.journal_data)

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
        if not self.journal_app:
            journal_window = tk.Toplevel(self.root)
            journal_window.title("Journal")
            self.journal_app = JournalApp(journal_window)

        self.journal_app.show_journal_window()  # Make sure to call this method to show the journal window

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
