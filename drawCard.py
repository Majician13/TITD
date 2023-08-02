import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shuffle

# Define the values and suits for the cards
values = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
suits = ['c', 'h', 's', 'd']

# Set the correct images directory path
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "cards")

# Function to load card images
def load_card_images():
    card_images = {}
    for value in values:
        for suit in suits:
            image_path = os.path.join(IMAGE_DIR, f"{value}{suit}.png")
            try:
                img = Image.open(image_path)
                card_images[value + suit] = img
            except Exception as e:
                print(f"Error loading image '{image_path}': {e}")
    return card_images

# Main application window for drawing cards
class DrawCardApp:
    def __init__(self, root):
        self.root = root

        self.shuffled_deck = shuffle.shuffled_cards
        self.card_images = load_card_images()

    def draw_card(self, card_label):
        drawn_card = shuffle.draw_next_card()
        if drawn_card:
            img = ImageTk.PhotoImage(self.card_images[drawn_card])
            card_label.config(image=img, text=f"Drawn Card: {drawn_card}")
            card_label.image = img
        else:
            text = "Card deck is empty"
            card_label.config(text=text, image=None)
