import os
import unittest
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main
import shuffle
import drawCard
import dice
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
        dice_images = dice.roll_dice(3)
        self.assertEqual(len(dice_images), 3)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == "__main__":
    unittest.main()
    atexit.register(dice.close_dice_images)  # Ensure dice images are closed when testing is done
