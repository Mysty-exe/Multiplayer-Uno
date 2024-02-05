#Imports required modules
from project.card import Pile, Deck, Hand, Card
from project.math import Vector
import project.constants as constants
 
class Game:
    def __init__(self):
        """
        Represents a Game object

        Attributes
            x (num): x coord
            y (num): y coord
        """
        self.ready = False #Checks if both players are loaded up
        #All the game data needed for the game to work
        self.pile = Pile([], Vector(constants.MIDPOINT.x - Card.size[0] / 2, constants.MIDPOINT.y - Card.size[1] / 2))
        self.draw_deck = Deck([], Vector(self.pile.pos.x + 180, self.pile.pos.y), 108)
        self.draw_deck.start_deck()
        self.hand1 = Hand(1)
        self.hand2 = Hand(2)
        self.hand1.create_hand(self.draw_deck.cards)
        self.hand2.create_hand(self.draw_deck.cards)
        self.pile.start_pile(self.draw_deck)

        self.won = False #Checks who won
        self.current_player = 1 #Checks which player is currently handling the object
        self.turn = 1 #Checks whose turn it is
