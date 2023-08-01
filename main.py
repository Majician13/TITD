import random
import os
import pygame
import pygame_gui
import dice
import shuffle
import drawCard

# Set the correct working directory
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize pygame
pygame.init()

# Set up the window in resizable mode
window_size = (800, 600)
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("Torch in the Dark")

# Create the pygame_gui manager
manager = pygame_gui.UIManager(window_size)

# Load dice images
dice_images = [pygame.image.load(os.path.join("images", f"{i}spot.png")) for i in range(1, 7)]

# Create a list to store the drawn card images
drawn_card_images = []

# Create a surface to hold the drawn card images
drawn_cards_surface = pygame.Surface((100, 100))

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
    draw_button.enable()

# Function to draw a card
def draw_card():
    global shuffled_cards
    image, text = drawCard.get_drawn_card_info(shuffled_cards)
    if image:
        # Draw the card image on the surface
        card_position = (20 + (len(drawn_card_images) * 80), 20)  # Adjust the spacing between drawn card images
        drawn_cards_surface.blit(image, card_position)
        pygame.display.update()  # Update the display to show the card images
    else:
        print(text)
        draw_button.disable()  # Disable the "Draw Card" button when the deck is empty


# Function to roll the dice
def roll_dice():
    num_dice = dice_entry.get_text().strip()

    if not num_dice:
        return None

    try:
        num_dice = int(num_dice)
        dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        return dice_values
    except ValueError:
        return None

# Create buttons and labels
roll_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(350, window_size[1] - 50, 150, 40),  # Beside the draw button
    text="Roll Dice",
    manager=manager
)

dice_entry_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(350, window_size[1] - 125, 280, 20),  # Above the text entry box
    text="Enter the number of 6-sided dice:",
    manager=manager
)

dice_entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(350, window_size[1] - 100, 100, 30),  # Bottom left of the label
    manager=manager
)

dice_result_images = []
dice_result_rects = []

shuffle_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(10, window_size[1] - 50, 150, 40),  # Bottom left
    text="Shuffle Deck",
    manager=manager
)

draw_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(180, window_size[1] - 50, 150, 40),  # Beside the shuffle button
    text="Draw Card",
    manager=manager
)



# Main game loop
clock = pygame.time.Clock()
is_running = True
while is_running:
    time_delta = clock.tick(60) / 1000.0

    dice_values = None  # Define dice_values here to avoid NameError

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            is_running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resize event
            window_size = event.size
            window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
            manager = pygame_gui.UIManager(window_size)

        # Process GUI events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == shuffle_button:
                    # Shuffle the cards
                    shuffle_deck()
                    drawn_card_images.clear()  # Clear the drawn_card_images list after shuffling
                elif event.ui_element == draw_button:
                    # Draw a card
                    draw_card()
                elif event.ui_element == roll_button:
                    # Roll the dice
                    num_dice = dice_entry.get_text().strip()
                    dice_values = roll_dice()  # Get the return value from roll_dice()
                    dice_result_images = dice.roll_dice(num_dice)
                    dice_result_rects = dice.get_dice_rects(dice_result_images, 350, window_size[1] - 190)

    # Move this block outside the event loop to avoid the NameError
    if dice_values:
        dice_result_images.clear()
        dice_result_rects.clear()
        for value in dice_values:
            image = dice_images[value - 1]
            dice_result_images.append(image)
            rect = image.get_rect()
            dice_result_rects.append(rect)

    manager.process_events(event)
    manager.update(time_delta)
    window.fill((255, 255, 255))

    manager.draw_ui(window)

    # Blit the drawn card surface to the main window
    window.blit(drawn_cards_surface, (200, window_size[1] - 170))

    # Blit dice result images
    x_offset = 350
    y_offset = window_size[1] - 190
    for rect, image in zip(dice_result_rects, dice_result_images):
        rect.topleft = (x_offset, y_offset)
        window.blit(image, rect)
        x_offset += rect.width + 10

    pygame.display.update()

# Quit the pygame
pygame.quit()
