import random
import os
import tkinter as tk
from PIL import Image, ImageTk
import dice
import shuffle
import drawCard

# Set the correct working directory
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize tkinter
root = tk.Tk()
root.title("Torch in the Dark")

# Load dice images
dice_images = [ImageTk.PhotoImage(Image.open(f"images/{i}spot.png")) for i in range(1, 7)]

# Create a list to store the drawn card images
drawn_card_images = []

# Create a canvas to hold the drawn card images
drawn_cards_canvas = tk.Canvas(root, width=800, height=100)
drawn_cards_canvas.pack()

# Shuffle the deck and test its contents
shuffled_cards = []
shuffle.shuffle_cards()
shuffled_cards = shuffle.shuffled_cards[:]  # Initialize the shuffled_cards list
print("Initial Deck Contents:")
print(shuffled_cards)

# Function to shuffle the deck of cards
def shuffle_deck():
    shuffle.shuffle_cards()
    global shuffled_cards
    shuffled_cards = shuffle.shuffled_cards[:]  # Update the global variable
    print("Shuffled Deck Contents:")
    print(shuffled_cards)
    enable_draw_button()  # Enable the "Draw Card" button after shuffling

def enable_draw_button():
    draw_button.config(state=tk.NORMAL)

# Function to draw a card
def draw_card():
    global shuffled_cards
    image, text = drawCard.get_drawn_card_info(shuffled_cards)
    if image:
        # Draw the card image on the canvas
        card_position = (20 + (len(drawn_card_images) * 80), 20)  # Adjust the spacing between drawn card images
        drawn_cards_canvas.create_image(card_position[0], card_position[1], anchor=tk.NW, image=image)
        root.update()  # Update the display to show the card images
    else:
        print(text)
        draw_button.config(state=tk.DISABLED)  # Disable the "Draw Card" button when the deck is empty

# Function to roll the dice
def roll_dice():
    num_dice = dice_entry.get().strip()

    if not num_dice:
        return

    try:
        num_dice = int(num_dice)
        dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        dice_result_images = [dice_images[value - 1] for value in dice_values]
        display_dice_results(dice_result_images)
    except ValueError:
        return

def display_dice_results(dice_result_images):
    x_offset = 350
    y_offset = root.winfo_height() - 190
    for image in dice_result_images:
        drawn_cards_canvas.create_image(x_offset, y_offset, anchor=tk.NW, image=image)
        x_offset += image.width() + 10

# Create buttons and labels
shuffle_button = tk.Button(root, text="Shuffle Deck", command=shuffle_deck)
shuffle_button.pack(side=tk.LEFT, padx=10, pady=10)

draw_button = tk.Button(root, text="Draw Card", command=draw_card)
draw_button.pack(side=tk.LEFT, padx=10, pady=10)

dice_entry_label = tk.Label(root, text="Enter the number of 6-sided dice:")
dice_entry_label.pack(side=tk.LEFT, padx=10, pady=10)

dice_entry = tk.Entry(root)
dice_entry.pack(side=tk.LEFT, padx=10, pady=10)

roll_button = tk.Button(root, text="Roll Dice", command=roll_dice)
roll_button.pack(side=tk.LEFT, padx=10, pady=10)

# Main tkinter loop
root.mainloop()
