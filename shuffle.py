import random

values = ['a', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k']
suits = ['c', 'h', 's', 'd']

shuffled_cards = []

def shuffle_cards():
    """Shuffle the deck of cards."""
    global shuffled_cards
    try:
        all_cards = [value + suit for value in values for suit in suits]
        shuffled_cards = all_cards.copy()
        random.shuffle(shuffled_cards)
        print('Shuffled Cards: ', shuffled_cards)
    except Exception as e:
        print("Error shuffling cards:", e)

def draw_next_card():
    """Draw the next card from the shuffled deck."""
    if shuffled_cards:
        return shuffled_cards.pop(0)
    else:
        return None
