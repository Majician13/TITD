import random
import os
import pygame
import pygame_gui

# Initialize pygame
pygame.init()

# Set up the window
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Torch in the Dark")

# Create the pygame_gui manager
manager = pygame_gui.UIManager(window_size)

# Load dice images
dice_images = [pygame.image.load(os.path.join("images", f"{i}spot.png")) for i in range(1, 7)]

# Define the card suits and values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create a deck of cards
deck = [(value, suit) for value in values for suit in suits]

# Add two jokers to the deck
joker1 = ('Joker', 'Black')
joker2 = ('Joker', 'Red')
deck.append(joker1)
deck.append(joker2)

# Boolean variable to track whether "Shuffle Deck" has been pressed the first time
shuffled = False

# Boolean variable to track whether the game is running or not
game_running = False

# Function to toggle game state and change button text
def toggle_game_state():
    global game_running
    if not game_running:
        random.shuffle(deck)
        draw_button.set_text("Draw Card")
        shuffle_button.set_text("Stop Game")
        game_running = True
    else:
        reset_game()
        shuffle_button.set_text("Shuffle Deck")
        game_running = False

def reset_game():
    global deck
    deck = [(value, suit) for value in values for suit in suits]
    deck.append(joker1)
    deck.append(joker2)
    card_label.set_text("")
    dice_label.set_text("")
    inventory_entry.empty()
    skills_entry.empty()
    for checkbox in corruption_checkboxes + stress_checkboxes + stash_checkboxes + xp_checkboxes:
        checkbox.unselect()
    draw_button.set_text("Draw Card")
    draw_button.disable()

    # Clear the inventory grid
    inventory_frame.empty()

def draw_card():
    if deck:
        card = random.choice(deck)
        deck.remove(card)
        card_label.set_text(f"{card[0]} of {card[1]}")
    else:
        card_label.set_text("No more cards in the deck!")

def shuffle_deck():
    global shuffled
    if not shuffled:
        random.shuffle(deck)
        draw_button.set_text("Draw Card")
        draw_button.enable()
        shuffled = True
    else:
        reset_game()
        shuffle_button.set_text("Shuffle Deck")
        shuffled = False

def roll_dice():
    dice_input = dice_entry.get_text().strip()

    if not dice_input:
        # Display an error message or handle the case when no value is entered
        return

    num_dice = int(dice_input)
    dice_values = [random.randint(1, 6) for _ in range(num_dice)]
    dice_result = max(dice_values)

    # Determine whether it's a success, failure, or partial
    if dice_result == 6 and dice_values.count(6) > 1:
        dice_result = "Critical Success"
    elif dice_result == 6:
        dice_result = "Success"
    elif dice_result in (4, 5):
        dice_result = "Mixed Success"
    else:
        dice_result = "Fail"

    dice_label.set_text(dice_result)

def sort_items_by_size(items, sizes):
    item_sizes = sorted(zip(items, sizes), key=lambda x: int(x[1]), reverse=True)
    sorted_items, sorted_sizes = zip(*item_sizes)
    return sorted_items, sorted_sizes

def place_inventory():
    # Clear the previous inventory
    inventory_frame.empty()

    # Get user-defined inventory items and sizes
    inventory_data = inventory_entry.get_text().strip().split("\n")

    inventory_items = []
    inventory_sizes = []

    for data in inventory_data:
        item, size = data.split(',')
        inventory_items.append(item.strip())
        inventory_sizes.append(size.strip())

    # Sort items based on sizes
    inventory_items, inventory_sizes = sort_items_by_size(inventory_items, inventory_sizes)

    current_row, current_column = 0, 0
    for i, item in enumerate(inventory_items):
        size = int(inventory_sizes[i]) if i < len(inventory_sizes) else 1
        size = max(1, min(size, 3))  # Ensure size is within the range of 1 to 3

        label = pygame_gui.elements.UIImage(
            relative_rect=pygame.Rect(current_column * 100, current_row * 30, size * 100, 30),
            image_surface=dice_images[dice_result - 1],
            manager=manager
        )

        current_column += size
        if current_column > 2:
            current_row += 1
            current_column = 0

# Create buttons and labels
shuffle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 10, 150, 40),
    text="Shuffle Deck",
    manager=manager
)

draw_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 60, 150, 40),
    text="Draw Card",
    manager=manager
)

card_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 110, 400, 40),
    text="",
    manager=manager
)

dice_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(10, 160, 300, 120),
    manager=manager
)

dice_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 5, 280, 20),
    text="Enter the number of 6-sided dice:",
    manager=manager,
    container=dice_frame
)

dice_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 30, 280, 30),
    manager=manager,
    container=dice_frame
)

roll_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 70, 280, 40),
    text="Roll Dice",
    manager=manager,
    container=dice_frame
)

dice_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 110, 280, 60),
    text="",
    manager=manager
)

inventory_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 290, 400, 20),
    text="Enter Inventory Items and Sizes (one per line, separated by comma):",
    manager=manager
)

inventory_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 315, 380, 100),
    manager=manager
)

place_inventory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, 425, 150, 40),
    text="Place Inventory",
    manager=manager
)

inventory_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(10, 475, 380, 100),
    manager=manager
)

corruption_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(10, 590, 400, 30),
    manager=manager
)

corruption_checkboxes = []
for i in range(6):
    checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(i * 60, 0, 50, 30),
        text=f"Corruption {i + 1}",
        manager=manager,
        container=corruption_frame
    )
    corruption_checkboxes.append(checkbox)

stress_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(420, 590, 400, 30),
    manager=manager
)

stress_checkboxes = []
for i in range(6):
    checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(i * 60, 0, 50, 30),
        text=f"Stress {i + 1}",
        manager=manager,
        container=stress_frame
    )
    stress_checkboxes.append(checkbox)

stash_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(10, 630, 500, 80),
    manager=manager
)

stash_checkboxes = []
for i in range(20):
    checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(i % 5 * 90, i // 5 * 40, 80, 30),
        text=f"Stash {i + 1}",
        manager=manager,
        container=stash_frame
    )
    stash_checkboxes.append(checkbox)

xp_frame = pygame_gui.elements.UIPanel(
    relative_rect=pygame.Rect(520, 630, 260, 80),
    manager=manager
)

xp_checkboxes = []
for i in range(10):
    checkbox = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(i % 5 * 50, i // 5 * 40, 40, 30),
        text=f"XP {i + 1}",
        manager=manager,
        container=xp_frame
    )
    xp_checkboxes.append(checkbox)

skills_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(10, 720, 400, 20),
    text="Enter up to 10 Skills (one per line):",
    manager=manager
)

skills_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(10, 745, 380, 150),
    manager=manager
)

conditions_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(420, 720, 400, 20),
    text="Enter up to 10 Conditions (one per line):",
    manager=manager
)

conditions_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(420, 745, 380, 150),
    manager=manager
)

# Main game loop
clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == shuffle_button:
                shuffle_deck()
            elif event.ui_element == draw_button:
                draw_card()
            elif event.ui_element == roll_button:
                try:
                    dice_result = int(dice_label.text)
                    dice_image = dice_images[dice_result - 1]
                    window.blit(dice_image, (10, 210))  # Updated blit position here
                except ValueError:
                    pass
        manager.process_events(event)

    manager.update(time_delta)
    window.fill((255, 255, 255))

    manager.draw_ui(window)

    # Draw the dice value as an image (if rolled)
    if dice_label.text != "":
        try:
            dice_result = int(dice_label.text)  # Fix on line 333
            dice_image = dice_images[dice_result - 1]
            window.blit(dice_image, (10, 210))  # Updated blit position here
        except ValueError:
            pass

    pygame.display.update()

pygame.quit()

