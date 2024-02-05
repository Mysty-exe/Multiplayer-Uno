#Imports needed
import pygame
import random
import pickle
import project.constants as constants
import project.card as card
from project.math import Vector
from project.ui import MenuUI, GameUI, Button
from project.network import Network
from project.sound import Sound

class Client:

    def __init__(self):
        self.width, self.height = constants.GAME_WIDTH, constants.GAME_HEIGHT #Set game width and height
        self.display = pygame.Surface((self.width, self.height)) #Display Surface
        self.blanket = pygame.Surface((self.width, self.height)) #Transition Surface
        self.trans_state = None
        self.blacken_var = 0
        
        #Images
        self.menu_bg = pygame.image.load('assets/background.png').convert()
        self.menu_bg = pygame.transform.scale(self.menu_bg, (self.width, self.height))
        self.background = pygame.image.load(f'assets/bg{random.randint(1, 5)}.png').convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.instructions_txt = pygame.image.load('assets/instructions.png').convert_alpha()
        self.instructions_txt = pygame.transform.scale(self.instructions_txt, (500, 500))

        #Mouse Vectors
        self.mouse_pos = Vector(0, 0)
        self.mouse_increment = Vector(0, 0)

        #UIs
        self.menu_ui = MenuUI(self.display)
        self.game_ui = GameUI(self.display)

        #Buttons
        self.play_btn = Button(self.display, 'Play')
        self.instructions_btn = Button(self.display, 'Instructions')
        self.quit_btn = Button(self.display, 'Quit')

        self.tutorial = ['arrowkey']

        self.network = None
        self.game = None
        self.pile = None
        self.draw_deck = None
        self.hand1 = None
        self.hand2 = None
        self.ready = False
        self.full = 'Not Full'

    def set_game(self):
        """Game variables needed to reset"""
        self.network = Network() #Set Network class
        self.won = None 
        self.timer = 0

    def transition(self, screen, sound, state):
        """
        #Darkens the screen
        Args:
            screen (object)
            sound (object)
            state (str)
        Returns:
            (str)
            returns the state
        """

        pygame.mouse.set_visible(True) #Make mouse invisible
        screen.blit(self.display, (0, 0)) #Draw display surface on screen
        self.blacken_var += 15

        self.blanket.set_alpha(self.blacken_var) #Make screen get darker
        self.display.blit(self.blanket, (0,0)) #Draw blanket on screen

        if self.blacken_var == 255: #Check if screen is fully black
            self.trans_state = 'Lighten'
            state = state.split()[-1] #Change state
            sound.transition.play() #Play sound

        return state

    def menu(self, screen, events, state):
        """
        #Runs the menu
        Args:
            screen (object)
            events (list)
            state (str)
        Returns:
            (str)
            returns the state
        """

        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.trans_state == 'Lighten':
            self.blacken_var -= 15

        screen.blit(self.display, (0, 0)) #Draw display to screen
        self.display.blit(self.menu_bg, (0, 0)) #Draw background

        pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) #Get Mouse coord
        self.mouse_increment = pos - self.mouse_pos #Get how much the mouse moved from past frame
        self.mouse_pos = pos

        pressed = False
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP: #Check if Mouse button was released
                pressed = True 

        #Draw title and buttons
        self.menu_ui.draw_title()
        play = self.play_btn.draw((150, 325), (self.mouse_pos.x, self.mouse_pos.y), pressed)
        instructions = self.instructions_btn.draw((150, 475), (self.mouse_pos.x, self.mouse_pos.y), pressed)
        quit = self.quit_btn.draw((150 , 625), (self.mouse_pos.x, self.mouse_pos.y), pressed)

        self.blanket.set_alpha(self.blacken_var) #Make screen go lighter
        self.display.blit(self.blanket, (0,0)) #Draw blanket to screen

        if not self.blacken_var and self.trans_state == 'Lighten':
            self.trans_state = None

        #Check which button was pressed
        if play:
            self.set_game()
            self.full = self.network.connect()
            state = 'Transition - Game'

        if instructions:
            state = 'Transition - Instructions'

        elif quit:
            state = 'Quit'

        return state
    
    def instructions(self, screen, events, state):
        """
        #Runs the instructions
        Args:
            screen (object)
            events (list)
            state (str)
        Returns:
            (str)
            returns the state
        """

        if self.trans_state == 'Lighten':
            self.blacken_var -= 15

        #Draw images
        screen.blit(self.display, (0, 0))
        self.display.blit(self.menu_bg, (0, 0))
        self.display.blit(self.instructions_txt, (50, 125))
        self.menu_ui.draw_back()

        #Set mouse coords
        pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.mouse_increment = pos - self.mouse_pos
        self.mouse_pos = pos

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Check if escape was pressed
                state = 'Transition - Menu'

        self.blanket.set_alpha(self.blacken_var) #Screen gets lighter
        self.display.blit(self.blanket, (0,0)) #Draw blanket to display

        if not self.blacken_var and self.trans_state == 'Lighten':
            self.trans_state = None

        return state

    def run(self, screen, sound, events, state):
        """
        #Runs the instructions
        Args:
            screen (object)
            sound (object)
            events (list)
            state (str)
        Returns:
            (str)
            returns the state
        """

        #Draw display and background
        screen.blit(self.display, (0, 0))
        self.display.fill(constants.COLOURS['white'])
        self.display.blit(self.background, (0, 0))

        if self.full == 'Full':
            if self.trans_state == 'Lighten':
                self.blacken_var -= 15
            self.display.fill(constants.COLOURS['black'])
            self.game_ui.draw_full()
            self.game_ui.draw_leave()
            self.blanket.set_alpha(self.blacken_var) #Screen gets lighter
            self.display.blit(self.blanket, (0,0)) #Draw blanket on display
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return 'Transition - Menu'
    
        elif not self.network.connected:
            self.blanket.set_alpha(self.blacken_var) #Screen gets lighter
            self.display.blit(self.blanket, (0,0)) #Draw blanket on display
            #Draw text
            self.game_ui.draw_not_connected()
            self.game_ui.draw_retry()
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #Check if enter is pressed
                    self.network.connect()
        else:
            try:
                self.game = self.network.send("get, None, None") #Send get to the server
            except Exception as e:
                print(e)
                self.network.connected = False #Set network connection to false
                return state

            if self.game == None:
                try:
                    self.network.send('disconnect, None, None') #Send disconnect to the server
                except Exception as e:
                    print(e)
                return 'Transition - Menu'

            #parse through game object
            self.ready = self.game.ready
            self.pile = self.game.pile
            self.draw_deck = self.game.draw_deck
            self.hand1 = self.game.hand1
            self.hand2 = self.game.hand2
            current_player = self.game.current_player
            turn = self.game.turn

            if self.game.won and self.game.won != current_player:
                self.won = False #Player didn't win
                self.network.send('disconnect, None, None') #Send disconnect to server
                return 'Transition - End'

            if not self.ready: #If Player 2 didn't join yet
                self.blanket.set_alpha(self.blacken_var) #Lighten screen if still transitioning
                self.display.blit(self.blanket, (0,0)) #Blit blanket
                self.game_ui.draw_waiting() #Draw text

            else:
                if self.trans_state == 'Lighten':
                    self.blacken_var -= 15

                self.timer += 1

                #Set mouse vectors
                pos = Vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                self.mouse_increment = pos - self.mouse_pos
                self.mouse_pos = pos

                #Draw text
                self.game_ui.draw_turn(turn)
                self.game_ui.draw_player(current_player)
                if current_player == 1:
                    if len(self.hand1.cards) > 13 and 'arrowkey' in self.tutorial: #Check if 13 cards in one screen
                        self.game_ui.draw_arrowkey() #Draw arrowkey text
                        if self.hand1.num > 1:
                            self.tutorial.remove('arrowkey') 
                else:
                    if len(self.hand2.cards) > 13 and 'arrowkey' in self.tutorial: #Check if 13 cards in one screen
                        self.game_ui.draw_arrowkey() #Draw arrowkey text
                        if self.hand2.num > 1:
                            self.tutorial.remove('arrowkey')
    
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Check if mouse button pressed
                        if current_player == 1 and turn == 1: #Check if it's player 1 and it's his/her turn
                            self.hand1.draw_new_card(self.mouse_pos, self.draw_deck, self.network, sound) #Check if player 1 can draw a new card
                            self.hand1.is_dragging(self.mouse_pos, self.network) #Check if a card can be dragged
                        elif current_player == 2 and turn == 2: #Check fi it's player 2 and it's his/her turn
                            self.hand2.draw_new_card(self.mouse_pos, self.draw_deck, self.network, sound) #Check if player 2 can draw a new card
                            self.hand2.is_dragging(self.mouse_pos, self.network) #Check if a card can be dragged
                    elif event.type == pygame.MOUSEBUTTONUP: #Check if mouse button has been released
                        if current_player == 1 and turn == 1: #Check if it's player 1 and it's his/her turn
                            self.hand1.can_place(constants.MIDPOINT, self.pile, self.network) #Check if card can be placed on pile
                            self.hand1.not_dragging(self.network) #Check if a card was being dragged
                        elif current_player == 2 and turn == 2: #Check if it's player 2 and it's his/her turn
                            self.hand2.can_place(constants.MIDPOINT, self.pile, self.network) #Check if card can be placed on pile
                            self.hand2.not_dragging(self.network) #Check if a card was being dragged

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                        if current_player == 1: #Check if it's player 1 and it's his/her turn
                            self.hand1.change_current('r', self.network) #Change slider if first screen is filled
                        else:
                            self.hand2.change_current('r', self.network)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                        if current_player == 1: #Check if it's player 1 and it's his/her turn
                            self.hand1.change_current('l', self.network) #Change slider left to see your other cards
                        else:
                            self.hand2.change_current('l', self.network)

                #Draw draw deck and pile
                self.draw_deck.draw_deck(self.display)
                self.pile.draw_pile(self.display)
                self.draw_deck.reset_deck(self.network) #Reset draw deck if it runs out

                #Draw the hands
                self.hand1.draw(self.display, current_player)
                self.hand2.draw(self.display, current_player)

                if current_player == 1: #Check if it's player 1 and it's his/her turn
                    self.hand2.draw_drag_card(self.display) #Draw card being dragged of the other player
                    self.hand1.hovering_over(self.draw_deck, self.mouse_pos) #Check if mouse is hovering over hand or draw deck
                    if turn == 1:
                        self.hand1.reformat_hand() #Reformat the hand
                        self.hand1.drag_card(self.display, self.mouse_increment, self.network, sound) #Drag card if conditions met
                else:
                    self.hand1.draw_drag_card(self.display)
                    self.hand2.hovering_over(self.draw_deck, self.mouse_pos)
                    if turn == 2:
                        self.hand2.reformat_hand()
                        self.hand2.drag_card(self.display, self.mouse_increment, self.network, sound)

                if current_player == 1: #Check if it's player 1 and it's his/her turn
                    won = self.hand1.game_finished() #Check if the player has 1 (Has no more cards)
                else:
                    won = self.hand2.game_finished()
                
                if won:
                    self.won = True
                    self.network.send('Won, None, None') #Send Won to the server
                    state = 'Transition - End' #Send to end screen

                self.blanket.set_alpha(self.blacken_var) #Screen lightens if still transitioning
                self.display.blit(self.blanket, (0,0)) #Draw blanket to display

                if not self.blacken_var and self.trans_state == 'Lighten':
                    self.trans_state = None

        return state
                
    def end(self, screen, events, state):
        """
        #Runs the end screen
        Args:
            screen (object)
            events (list)
            state (str)
        Returns:
            (str)
            returns the state
        """

        if self.trans_state == 'Lighten':
            self.blacken_var -= 15

        screen.blit(self.display, (0, 0)) #Draw display
        self.display.fill(constants.COLOURS['black']) #Fill blanket
        self.menu_ui.draw_back() #Draw text
        #Draw Win or Lose text
        if self.won:
            self.menu_ui.draw_over('Won')
        else:
            self.menu_ui.draw_over('Lost')

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: #Check if escape is pressed
                self.network.send("disconnect, None, None")
                state = 'Transition - Menu'

        self.blanket.set_alpha(self.blacken_var) #Make screen go lighter
        self.display.blit(self.blanket, (0,0)) #Draw blanket on display

        if not self.blacken_var and self.trans_state == 'Lighten':
            self.trans_state = None

        return state
