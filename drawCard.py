import os
import pygame
import random

# Define the values and suits for the cards
values = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
suits = ['c', 'h', 's', 'd']

# Set the correct images directory path
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "cards")

# Load card images
card_images = {}
for value in values:
    for suit in suits:
        card_images[value + suit] = pygame.image.load(os.path.join(IMAGE_DIR, f"{value}{suit}.png"))
        
# Function to load card images
def load_card_images():
    card_images = {}
    for value in values:
        for suit in suits:
            image_path = os.path.join(IMAGE_DIR, f"{value}{suit}.png")
            try:
                card_images[value + suit] = pygame.image.load(image_path)
            except pygame.error as e:
                print(f"Error loading image '{image_path}': {e}")
    return card_images

# Load card images
card_images = load_card_images()

# Function to draw the next card from the shuffled deck
def draw_next_card(shuffled_deck):
    if shuffled_deck:
        return shuffled_deck.pop(0)
    else:
        return None

# Function to get the image and text of the drawn card
def get_drawn_card_info(shuffled_deck):
    drawn_card = draw_next_card(shuffled_deck)
    if drawn_card:
        image = card_images[drawn_card]
        text = f"Drawn Card: {drawn_card}"
        return image, text
    else:
        text = "Card deck is empty"
        return None, text
