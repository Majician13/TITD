import random

# Define the values and suits for the cards
values = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
suits = ['c', 'h', 's', 'd']

# Create a list to store the shuffled cards
shuffled_cards = []

# Function to shuffle the cards
def shuffle_cards():
    global shuffled_cards
    # Generate all possible combinations of values and suits
    all_cards = [value + suit for value in values for suit in suits]

    # Randomly shuffle the cards
    shuffled_cards = all_cards.copy()
    random.shuffle(shuffled_cards)

# Function to draw the next card from the shuffled deck
def draw_next_card():
    if shuffled_cards:
        return shuffled_cards.pop(0)
    else:
        return None
