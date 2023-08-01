import random
import os
import pygame

# Load dice images
dice_images = [pygame.image.load(os.path.join("images", f"{i}spot.png")) for i in range(1, 7)]

def roll_dice(num_dice):
    if not num_dice:
        return []

    try:
        num_dice = int(num_dice)
        dice_values = [random.randint(1, 6) for _ in range(num_dice)]
        return [dice_images[value - 1] for value in dice_values]
    except ValueError:
        return []

def get_dice_rects(dice_images, x_offset, y_offset):
    dice_rects = []
    for image in dice_images:
        rect = image.get_rect()
        rect.topleft = (x_offset, y_offset)
        dice_rects.append(rect)
        x_offset += rect.width + 10
    return dice_rects
