import random
import tkinter as tk
from tkinter import ttk

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
        draw_button.config(text="Draw Card", state="normal")
        shuffle_button.config(text="Stop Game")
        game_running = True
    else:
        reset_game()
        shuffle_button.config(text="Shuffle Deck")
        game_running = False

def reset_game():
    global deck
    deck = [(value, suit) for value in values for suit in suits]
    deck.append(joker1)
    deck.append(joker2)
    card_label.config(text="")
    dice_label.config(text="")
    inventory_entry.delete("1.0", tk.END)
    skills_entry.delete("1.0", tk.END)
    for checkbox in corruption_checkboxes + stress_checkboxes + stash_checkboxes + xp_checkboxes:
        checkbox.set("")
    draw_button.config(text="Draw Card", state="disabled")

    # Clear the inventory grid
    for child in inventory_frame.winfo_children():
        child.destroy()

def draw_card():
    if deck:
        card = random.choice(deck)
        deck.remove(card)
        card_label.config(text=f"{card[0]} of {card[1]}")
    else:
        card_label.config(text="No more cards in the deck!")

def shuffle_deck():
    global shuffled
    if not shuffled:
        random.shuffle(deck)
        draw_button.config(text="Draw Card", state="normal")
        shuffled = True
    else:
        reset_game()
        shuffle_button.config(text="Shuffle Deck")
        shuffled = False

def roll_dice():
    dice_input = dice_entry.get().strip()

    if not dice_input:
        # Display an error message or handle the case when no value is entered
        return

    num_dice = int(dice_input)
    dice_values = [random.randint(1, 6) for _ in range(num_dice)]
    dice_result = ", ".join(str(value) for value in dice_values)

    if max(dice_values) == 6 and dice_values.count(6) > 1:
        dice_result += " (Critical Success)"
    elif max(dice_values) == 6:
        dice_result += " (Success)"
    elif max(dice_values) in (4, 5):
        dice_result += " (Mixed Success)"
    else:
        dice_result += " (Fail)"

    dice_label.config(text=dice_result)

def sort_items_by_size(items, sizes):
    item_sizes = sorted(zip(items, sizes), key=lambda x: int(x[1]), reverse=True)
    sorted_items, sorted_sizes = zip(*item_sizes)
    return sorted_items, sorted_sizes

def place_inventory():
    # Clear the previous inventory
    for child in inventory_frame.winfo_children():
        child.destroy()

    # Get user-defined inventory items and sizes
    inventory_data = inventory_entry.get("1.0", tk.END).strip().split("\n")

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

        label = tk.Label(inventory_frame, text=f"{item}", borderwidth=1, relief="solid", padx=5, pady=5)
        label.grid(row=current_row, column=current_column, rowspan=1, columnspan=size, sticky="nsew")

        current_column += size
        if current_column > 2:
            current_row += 1
            current_column = 0

# Main application window
root = tk.Tk()
root.title("Torch in the Dark")
root.geometry("800x600")  # Set the window size

# Create themed styles
style = ttk.Style()
style.configure("TButton", padding=10, relief="flat", font=("Helvetica", 12))

# Create a label frame to group shuffle button, draw card button, and card value results
card_box = ttk.LabelFrame(root, text="Card Actions and Results", relief="solid", borderwidth=1)
card_box.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

# Shuffle Button
shuffle_button = ttk.Button(card_box, text="Shuffle Deck", command=toggle_game_state)
shuffle_button.grid(row=0, column=0, pady=10, padx=10)

# Draw Card Button (Initially disabled)
draw_button = ttk.Button(card_box, text="Draw Card", command=draw_card, state="disabled")
draw_button.grid(row=1, column=0, pady=10, padx=10)

# Card Label
card_label = ttk.Label(card_box, text="", font=("Helvetica", 20))
card_label.grid(row=2, column=0, pady=10)

# Dice Frame
dice_frame = ttk.Frame(root, padding=5, relief="solid", borderwidth=1)
dice_frame.grid(row=0, column=1, columnspan=2, pady=5)

dice_entry_label = ttk.Label(dice_frame, text="Enter the number of 6-sided dice:", font=("Helvetica", 12))
dice_entry_label.grid(row=0, column=1, columnspan=2, pady=5)

dice_entry = ttk.Entry(dice_frame, font=("Helvetica", 12))
dice_entry.grid(row=1, column=1, columnspan=1, pady=5)

roll_button = ttk.Button(dice_frame, text="Roll Dice", command=roll_dice)
roll_button.grid(row=2, column=1, pady=5, padx=5)

# Dice Result Label
dice_label = ttk.Label(dice_frame, text="", font=("Helvetica", 14))
dice_label.grid(row=3, column=1, columnspan=2, pady=10)

# Inventory Entry
inventory_label = ttk.Label(root, text="Enter Inventory Items and Sizes (one per line, separated by comma):", font=("Helvetica", 12))
inventory_label.grid(row=6, column=0, columnspan=2, pady=5)
inventory_entry = tk.Text(root, height=5, width=40, font=("Helvetica", 12))
inventory_entry.grid(row=7, column=0, columnspan=2, pady=5)

# Inventory Frame
inventory_frame = tk.Frame(root, borderwidth=1, relief="solid", bg="lightgray")
inventory_frame.grid(row=8, column=0, columnspan=2, pady=10, padx=20)

# Place Inventory Button
place_inventory_button = ttk.Button(root, text="Place Inventory", command=place_inventory)
place_inventory_button.grid(row=9, column=0, columnspan=2, pady=10)

# Checkboxes for Corruption
corruption_frame = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
corruption_frame.grid(row=10, column=0, pady=10, padx=10, sticky="w")

corruption_checkboxes = []
for i in range(6):
    c = tk.StringVar()
    checkbox = tk.Checkbutton(corruption_frame, text=f"Corruption {i+1}", variable=c, onvalue=f"Corruption {i+1}", offvalue="")
    checkbox.pack(side=tk.LEFT, padx=5)
    corruption_checkboxes.append(c)

# Checkboxes for Stress
stress_frame = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
stress_frame.grid(row=10, column=1, pady=10, padx=10, sticky="e")

stress_checkboxes = []
for i in range(6):
    s = tk.StringVar()
    checkbox = tk.Checkbutton(stress_frame, text=f"Stress {i+1}", variable=s, onvalue=f"Stress {i+1}", offvalue="")
    checkbox.pack(side=tk.LEFT, padx=5)
    stress_checkboxes.append(s)

# Checkboxes for Stash
stash_frame = ttk.LabelFrame(root, text="Stash")
stash_frame.grid(row=2, column=0, columnspan=4, pady=5, padx=10)
stash_checkboxes = []
for i in range(20):
    c = tk.StringVar()
    checkbox = tk.Checkbutton(stash_frame, text=f"Stash {i+1}", variable=c, onvalue=f"Stash {i+1}", offvalue="")
    checkbox.grid(row=i // 5, column=i % 5, padx=5, pady=2, sticky="w")
    stash_checkboxes.append(c)

# Checkboxes for XP
xp_frame = ttk.LabelFrame(root, text="XP")
xp_frame.grid(row=3, column=0, columnspan=4, pady=5, padx=10)
xp_checkboxes = []
for i in range(10):
    c = tk.StringVar()
    checkbox = tk.Checkbutton(xp_frame, text=f"XP {i+1}", variable=c, onvalue=f"XP {i+1}", offvalue="")
    checkbox.grid(row=i // 5, column=i % 5, padx=5, pady=2, sticky="w")
    xp_checkboxes.append(c)

# Skills Entry
skills_label = ttk.Label(root, text="Enter up to 10 Skills (one per line):", font=("Helvetica", 12))
skills_label.grid(row=11, column=0, columnspan=2, pady=5)

skills_entry = tk.Text(root, height=10, width=40, font=("Helvetica", 12))
skills_entry.grid(row=12, column=0, columnspan=2, pady=5)

# Conditions Entry
conditions_label = ttk.Label(root, text="Enter up to 10 Conditions (one per line):", font=("Helvetica", 12))
conditions_label.grid(row=11, column=2, columnspan=2, pady=5)

conditions_entry = tk.Text(root, height=10, width=40, font=("Helvetica", 12))
conditions_entry.grid(row=12, column=2, columnspan=2, pady=5)

root.mainloop()
