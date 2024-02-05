#Imports required modules
import os
from project.math import Vector
import pygame

#Constants needed for the game
GAME_TITLE = 'Uno'
GAME_WIDTH = 1100
GAME_HEIGHT = 800
MIDPOINT = Vector(GAME_WIDTH / 2, GAME_HEIGHT / 2)
GAME_FPS = 15
COLOURS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 220, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "indigo": (75, 0, 130),
    "magenta": (255, 0, 255),
    "lime": (118, 186, 27),
    "grey": (24, 25, 26),
    "light grey": (97, 97, 97),
    "light blue": (38, 171, 255),
    "red2": (229, 57, 53),
    "purple": (124, 82, 149),
    "gold": (255, 218, 0)
}
HAND_COORDS = [475, 437.5, 400, 362.5, 325, 287.5, 250, 212.5, 175, 137.5, 100, 62.5, 25]

#Create screen needed to load up images
pygame.display.set_mode((1,1), pygame.NOFRAME)

cards = {"flipped": pygame.image.load("assets/flipped.png").convert_alpha()}

for fn in os.listdir('assets/Cards'): #Loops through folder of cards
    f = os.path.join('assets/Cards', fn)
    if os.path.isfile(f) and f.endswith('png'): #Checks if card is a png file
        cards[f"{f}"] = pygame.image.load(f).convert_alpha() #Puts the card in the dicitonary

for card in cards.keys():
    #Resizes all the cards to (150, 200)
    cards[card] = pygame.transform.scale(cards[card], (150, 200))

#Deletes screen
pygame.quit()
