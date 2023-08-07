from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import ttk
import shuffle

class DrawCardApp:
    def __init__(self, root, journal_app):
        self.root = root
        self.journal_app = journal_app
        self.card_label = None

        self.draw_button = ttk.Button(self.root, text="Draw Card", command=self.draw_card)
        self.draw_button.pack(side="left", padx=10, pady=10)

    def draw_card(self):
        drawn_card = shuffle.draw_next_card()
        if drawn_card:
            card_image_path = os.path.join("images", "cards", drawn_card + ".png")
            print(drawn_card)
            if os.path.exists(card_image_path):
                card_image = Image.open(card_image_path)
                card_photo = ImageTk.PhotoImage(card_image)

                if self.card_label:
                    self.card_label.destroy()

                self.card_label = ttk.Label(self.root, image=card_photo)
                self.card_label.photo = card_photo
                self.card_label.pack()

                if self.journal_app:
                    self.journal_app.add_entry("Draw Card", f"Drawn Card: {drawn_card}", "red")
                    self.journal_app.clear_entries("Draw Card Value")  # Clear previous "Card Value" entries
