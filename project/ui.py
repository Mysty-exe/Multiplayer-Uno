#Imports required modules
import pygame
import project.constants as constants

pygame.init() #Initializes pygame

class UI:
    def __init__(self, screen):
        """
        Represents a UI object

        Attributes
            screen (object): screen to draw text and buttons
            width (num): width of the game
            height (num): height of the game
            largefont (font object): Used to blit text
            font (font object): Used to blit text
            medfont (font object): Used to blit text
            smallfont (font object): Used to blit text
        """

        self.screen = screen
        
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT
        #Loads up the fonts needed
        self.largefont = pygame.font.Font('fonts/font.ttf', 200)
        self.font = pygame.font.Font('fonts/font.ttf', 60)
        self.medfont = pygame.font.Font('fonts/font.ttf', 40)
        self.smallfont = pygame.font.Font('fonts/font.ttf', 30)

class Button(UI):
    def __init__(self, screen, text):
        """
        Used to represent a button

        Attributes
            text (str): Text to put on button
            btn_width (num): Width of the button
            btn_height (num): Height of the button
        """

        UI.__init__(self, screen)

        self.text = text
        self.btn_width, self.btn_height = 300, 100

    def draw(self, pos, mouse, clicked):
        """
        Draws button on screen and checks if it was pressed
        Args:
            pos (tupple)
            mouse (tupple)
            clicked (boolean)
        Returns:
            (boolean)
        """
        button = pygame.Rect(pos[0], pos[1], self.btn_width, self.btn_height) #Makes the button into a rect
        color = constants.COLOURS['white']
        pressed = False
        if button.collidepoint(mouse): #Checks if mouse is over the button
            color = constants.COLOURS['black'] #Turns the button black
            if clicked: #Checks if mouse button is being actively clicked
                pressed = True
	
        txt = self.font.render(self.text, True, color) #Renders text
        txt_x, txt_y = pos[0] + ((300 / 2) - (txt.get_width() / 2)), pos[1] + 30
        self.screen.blit(txt, (txt_x, txt_y)) #Blits text to screen
        pygame.draw.rect(self.screen, color, button, 2, 3) #Draws button to screen
  
        return pressed

class MenuUI(UI):
    def __init__(self, screen):
        """
        Represents a Menu object
        Inherits from the UI class
        """

        UI.__init__(self, screen)

    def draw_title(self):
        """Draws Uno on the screen"""
        txt = self.largefont.render('UNO', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (175, 100)) #Draws the text

    def draw_back(self):
        """Draws "press ESC to go back to the Menu" to the screen"""
        txt = self.medfont.render('press ESC to go back to the Menu', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (10, 50)) #Draws the text

    def draw_over(self, end):
        """
        Draws text based on if you won or lost the game
        Args:
            end (str)
        Returns:
            (None)
        """
    
        txt = self.font.render(f'You {end} the Game', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (self.width / 2 - txt.get_width() / 2, self.height / 2 - txt.get_height() / 2)) #Draws the text

class GameUI(UI):
    def __init__(self, screen):
        """
        Represents a game object
        Inherits from the UI class
        """

        UI.__init__(self, screen)

    def draw_retry(self):
        """Draws "Press Enter to try and connect" to the screen"""
        txt = self.smallfont.render('Press Enter to try and connect', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (700, 700)) #Draws the text

    def draw_leave(self):
        """Draws "Press enter to go back" to the screen"""
        txt = self.smallfont.render('Press Enter to go back', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (700, 700)) #Draws the text

    def draw_full(self):
        """Draws "Gamae is full" to the screen"""
        txt = self.font.render('Game is Full', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (self.width / 2 - txt.get_width() / 2, self.height / 2 - txt.get_height() / 2)) #Draws the text

    def draw_waiting(self):
        """Draws "Waiting for a player to join" to the screen"""
        txt = self.font.render('Waiting For A Player To Join', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (self.width / 2 - txt.get_width() / 2, self.height / 2 - txt.get_height() / 2)) #Draws the text

    def draw_not_connected(self):
        """Draws "Server Down" to the screen"""
        txt = self.font.render('Server Down', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (self.width / 2 - txt.get_width() / 2, self.height / 2 - txt.get_height() / 2)) #Draws the text

    def draw_turn(self, turn):
        """
        Draws text based on who's turn it is
        Args:
            turn (num)
        Returns:
            (None)
        """

        #Checks whose turn it is
        if turn == 1:
            turn = 'One'
        else:
            turn = 'Two'
    
        txt = self.font.render(f'Player {turn}s Turn', True, constants.COLOURS['white']) #loads up text
        self.screen.blit(txt, (30, self.height / 2 - txt.get_height() / 2)) #Draws the text

    def draw_arrowkey(self):
        """Draws arrowkey text to the screen"""
        txt = self.smallfont.render('Use the Arrow Key to see the rest of your cards', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(txt, (30, 560)) #Draws the text

    def draw_player(self, p):
        """
        Draws text based on which player it is
        Args:
            p (num)
        Returns:
            (None)
        """

        #Checks which player it is
        player = None
        other_player = None
        if p == 1:
            player = 'One'
            other_player = 'Two'
        else:
            other_player = 'One'
            player = 'Two'

        player_text = self.smallfont.render(f'Player {player}', True, constants.COLOURS['white']) #Loads up text
        other_player_text = self.smallfont.render(f'Player {other_player}', True, constants.COLOURS['white']) #Loads up text
        self.screen.blit(player_text, (950, 560)) #Draws the text
        self.screen.blit(other_player_text, (30, 220)) #Draws the text
