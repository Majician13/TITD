import os
import unittest
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main
import shuffle
import drawCard
import dice
import char
import atexit

class TestTITDApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = tk.Tk()
        cls.app = main.MainApp(cls.root)

    def test_shuffle_deck(self):
        shuffle.shuffle_cards()
        shuffled_cards = shuffle.shuffled_cards
        self.assertTrue(len(shuffled_cards) == 52)
        
    def test_draw_card(self):
        card_label = ttk.Label(self.app.root)
        self.app.draw_card_app.draw_card(card_label)
        card_text = card_label.cget("text")
        self.assertIn("Drawn Card:", card_text)

    def test_roll_dice(self):
        dice_images, highest_dice, lowest_dice = dice.roll_dice(3, False)  # Pass the zero_negative argument
        self.assertEqual(len(dice_images), 3)

    def test_dice_images_not_defined(self):
        # Simulate the scenario where dice_images is not defined in the enclosing scope
        try:
            dice_images, highest_dice, lowest_dice, dice_values = dice.roll_dice(3, False)
        except NameError:
            self.fail("dice_images should be defined")

            
    def test_roll_dice(self):
        dice_images, highest_dice, lowest_dice, dice_values = dice.roll_dice(3, False)  # Pass the zero_negative argument
        
        self.assertEqual(len(dice_images), 3)
        self.assertTrue(1 <= highest_dice <= 6)
        self.assertTrue(1 <= lowest_dice <= 6)
        self.assertEqual(len(dice_values), 3)
        self.assertTrue(all(1 <= value <= 6 for value in dice_values))


    def test_character_sheet(self):
        char_window = tk.Toplevel(self.app.root)
        char_app = char.CharacterSheetApp(char_window)

        # Test setting and getting name
        test_name = "Test Character"
        char_app.name_entry.insert(0, test_name)
        self.assertEqual(char_app.name_entry.get(), test_name)

        # Test stress and corruption checkboxes
        for var in char_app.stress_vars:
            var.set(1)
        for var in char_app.corruption_vars:
            var.set(1)
        for var in char_app.stress_vars:
            self.assertEqual(var.get(), 1)
        for var in char_app.corruption_vars:
            self.assertEqual(var.get(), 1)

        # Test companions
        test_companion_names = ["Companion 1", "Companion 2", "Companion 3", "Companion 4", "Companion 5"]
        for entry, name in zip(char_app.companion_entries, test_companion_names):
            entry.insert(0, name)
        for vars in char_app.companion_vars:
            for var in vars:
                var.set(1)
        for entry, name in zip(char_app.companion_entries, test_companion_names):
            self.assertEqual(entry.get(), name)
        for vars in char_app.companion_vars:
            for var in vars:
                self.assertEqual(var.get(), 1)

        # Test XP checkboxes
        for var in char_app.xp_vars:
            var.set(1)
        for var in char_app.xp_vars:
            self.assertEqual(var.get(), 1)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == "__main__":
    unittest.main()
    atexit.register(dice.close_dice_images)  # Ensure dice images are closed when testing is done
