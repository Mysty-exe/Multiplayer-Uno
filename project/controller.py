#Import required modules
import pygame
import sys
from project.client import Client
import project.constants as constants
from project.sound import Sound


class GameInstance:

    def __init__(self):
        pygame.init() #Initialize Pygame

        #Set title and Icon
        self.title = constants.GAME_TITLE
        self.icon = pygame.image.load('assets/icon.png')
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)

        #Initialize Screen
        self.screen = pygame.display.set_mode((constants.GAME_WIDTH, constants.GAME_HEIGHT), 0, 32)

        #Make an instance of game class and sound class
        self.game_state = 'Menu'
        self.game = Client()
        self.sound = Sound()

        #Set fps and clock
        self.fps = constants.GAME_FPS
        self.dt = self.fps
        self.clock = pygame.time.Clock()

    def run(self):
        """Runs the whole game"""
        while self.game_state != 'Quit': #Loop till game_state == "Quit"
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.game_state = 'Quit'

            if self.game_state in ['Transition - Game', 'Transition - Instructions', 'Transition - Menu', 'Transition - End']:
                self.game_state = self.game.transition(self.screen, self.sound, self.game_state) #Game transition
            
            if self.game_state == 'Menu':
                self.game_state = self.game.menu(self.screen, events, self.game_state) #Game Menu

            if self.game_state == 'Instructions':
                self.game_state = self.game.instructions(self.screen, events, self.game_state) #Game Instructions

            if self.game_state == 'Game':
                self.game_state = self.game.run(self.screen, self.sound, events, self.game_state) #Runs the game

            if self.game_state == 'End':
                self.game_state = self.game.end(self.screen, events, self.game_state) #Game finished

            pygame.display.update() #Updates the screen
            self.dt = (self.clock.tick(self.fps) / 1000) * 60

        self.quit()

    def quit(self):
        """Quits the game"""
        #Quits the game
        pygame.quit()
        sys.exit()
