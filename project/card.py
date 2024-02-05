#Import required modules
import pygame
import random
import project.constants as constants
from project.math import Vector

class Pile:
    def __init__(self, cards, pos):
        self.cards = cards 
        self.pos = pos

    def start_pile(self, deck):
        if len(self.cards) == 0: #Check if pile is empty
            self.cards.append(deck.cards.pop()) #Add a card
            self.cards[0].flipped = False #Card isn't flipped
        self.cards[0].pos = self.pos #Set coord to pile coord

    def draw_pile(self, surface):
        for card in self.cards:
            if card.flipped:
                surface.blit(constants.cards["flipped"], (card.pos.x, card.pos.y)) #blit a flipped card
            else:
                surface.blit(constants.cards[card.card], (card.pos.x, card.pos.y)) #blit the actual card

class Deck:
    def __init__(self, cards, pos, num):
        self.cards = cards 
        self.pos = pos
        self.num = num

    def start_deck(self):
        for card in constants.cards.keys(): #Loop through cards in constant module
            if card == 'flipped':
                continue
            code = card[13:-4] #Get the name of the card
            #Parse the card info from the name
            types = code.split('-')
            self.cards.append(Card(self, types[0], types[1], types[2], card))

        random.shuffle(self.cards) #Shuffle the cards

    def draw_deck(self, surface):
        for card in self.cards:
            card.flipped = True
            if card.flipped:
                surface.blit(constants.cards["flipped"], (card.pos.x, card.pos.y))
            else:
                surface.blit(constants.cards[card.card], (card.pos.x, card.pos.y))

    def reset_deck(self, network):
        if len(self.cards) == 10:
            network.send('reset_deck, None, None') #Send reset_deck to server

            random.shuffle(self.cards) #Shuffle the cards

class Hand:
    def __init__(self, player):
        self.cards = []
        self.player = player
        self.num = 1

    def print_hand(self):
        for card in self.cards:
            print(card.pos.coord(), end=' ')
 
    def current_cards(self):
        length = len(self.cards)
        if length < self.num * 13: #Check if there are more cards than the screen can handle
            maximum = length
        else:
            maximum = self.num * 13
        minimum = (self.num * 13) - 13

        return minimum, maximum
    
    def change_current(self, direction, network):
        if direction == 'r' and len(self.cards) > self.num * 13:
            network.send('change-r, None, None') #Send change-r to server
        elif direction == 'l' and self.num > 1:
            network.send('change-l, None, None') #Send change-l to server
        self.reformat_hand() #Reformat hand

    def create_hand(self, deck):
        if len(self.cards) < 7:
            for _ in range(7):
                self.cards.append(deck.pop(random.randint(0, len(deck) - 1))) #Add card from deck to hand

    def draw_drag_card(self, surface):
        for card in self.cards:
            if card.dragging:
                card.flipped = True
                y = 590 - card.pos.y #Get the y flipped for the other player
                surface.blit(constants.cards["flipped"], (card.pos.x, 10 + y)) #draw the card
                break
    
    def draw(self, surface, player):
        minimum, maximum = self.current_cards() #Get the minimum and maximum card indexes on the screen

        flipped = False
        #Set the x depending on which hand and which player it is
        if player == 1:
            if self.player == 1:
                y = 590
                flipped = False
            else:
                y = 10
                flipped = True
        elif player == 2:
            if self.player == 1:
                y = 10
                flipped = True
            else:
                y = 590
                flipped = False

        for x, card in enumerate(self.cards[minimum:maximum]):
            num = constants.HAND_COORDS[len(self.cards[minimum:maximum]) - 1] + (75 * x) #Get the x coord
            
            if not card.dragging:
                card.pos = Vector(num, y) #Set the x and y

        for x, card in enumerate(self.cards[minimum:maximum]):
            card.flipped = flipped
            if card.dragging:
                continue
            if card.flipped:
                surface.blit(constants.cards["flipped"], (card.pos.x, card.pos.y)) #Draw flipped card
            else:
                surface.blit(constants.cards[card.card], (card.pos.x, card.pos.y)) #Draw the regular card

    def reformat_hand(self):
        minimum, maximum = self.current_cards() #Get minimum and maximum card indexes for the screen

        for x, card in enumerate(self.cards[minimum:maximum]):
            if card.dragging:
                continue
            num = constants.HAND_COORDS[len(self.cards[minimum:maximum]) - 1] + (75 * x) #Get the x coord
            card.pos = Vector(num, 590) #Set the coordinate
            card.flipped = False

    def is_dragging(self, mouse_pos, network):
        minimum, maximum = self.current_cards() #Get minimum and maximum card indexes for the screen

        for card in self.cards[minimum:maximum]:
            if card == self.cards[minimum:maximum][-1] or len(self.cards[minimum:maximum]) == 1: #Check if it's the last card or it there is only one card
                num = 150
            else:
                num = 75
            if pygame.Rect(card.pos.x, card.pos.y, num, 200).collidepoint((mouse_pos.x, mouse_pos.y)): #Check if mouse is hovering over card
                card.dragging = True
                network.send(f'start-dragging, {self.cards.index(card)}, None') #Send start-dragging to server
                break

    def can_drag(self):
        for card in self.cards:
            if card.dragging:
                return False #return False if a card is being dragged
        return True

    def not_dragging(self, network):
        for card in self.cards:
            if card.dragging:
                card.dragging = False
                network.send(f'stop-dragging, {self.cards.index(card)}, None') #Stop dragging

    def drag_card(self, display, increment, network, sound):
        for card in self.cards:
            if card.dragging:
                card.drag(display, increment, self, network) #Drag card with the increment
                break

    def can_place(self, midpoint, pile, network):
        minimum, maximum = self.current_cards() #Get minimum and maximum card indexes for the screen

        for x, card in enumerate(self.cards[minimum:maximum]):
            if card.dragging:
                coord = Vector(card.pos.x + 75, card.pos.y + 100) #Get the middle of the card
                if coord.distance(midpoint) < 100 and card.card_check(pile.cards[-1]): #Check if the card is close enough to the pile and it can be placed
                    index = self.cards.index(card) #Get card index
                    pile.cards.append(card) #Add card to pile
                    self.cards.remove(card) #Remove card from the hand 
                    card.dragging = False
                    card.pos = pile.pos
                    network.send(f'drag-to-pile, {index}, None') #Send drag-to-pile to server with the index
                else: #Card isn't close to the pile or isn't allowed to be placed
                    num = constants.HAND_COORDS[len(self.cards[minimum:maximum]) - 1] + (75 * x) #Get x coord
                    card.pos = Vector(num, 590) #Set card coord
                    card.dragging = False
                    network.send(f'reset-card, {self.cards.index(card)}, ({card.pos.x},{card.pos.y})') #Send reset-card to server

    def draw_new_card(self, mouse, deck, network, sound):
        if pygame.Rect(deck.pos.x, deck.pos.y, Card.size[0], Card.size[1]).collidepoint((mouse.x, mouse.y)): #Check if mouse is hovering over draw pile
            try:
                network.send('draw, None, None') #Send draw to the server
            except Exception as e:
                print(e)

    def hovering_over(self, deck, mouse):
        minimum, maximum = self.current_cards() #Get minimum and maximum card indexes for the screen
        hover_over_draw = False
        hover_over_hand = False

        if len(deck.cards) > 0: #Make sure draw deck is not empty
            if pygame.Rect(deck.pos.x, deck.pos.y, Card.size[0], Card.size[1]).collidepoint((mouse.x, mouse.y)): #Check if mouse is on draw deck
                hover_over_draw = True
            else:
                hover_over_draw = False

        for card in self.cards[minimum:maximum]:
            if pygame.Rect(card.pos.x, card.pos.y, Card.size[0], Card.size[1]).collidepoint((mouse.x, mouse.y)): #Check if mouse is on any of the cards
                hover_over_hand = True
                break
        else:
            hover_over_hand = False

        if hover_over_hand or hover_over_draw:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) #Switch mouse cursor depending on if the mouse is on the draw deck of hand
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
    def game_finished(self):
        if len(self.cards) < 1: #Check if player ran out of cards
            return True
        return False

class Card:
    
    size = (150, 200)

    def __init__(self, deck, colour, num, wild, card):
        self.deck = deck
        self.pos = Vector(self.deck.pos.x, self.deck.pos.y)
        self.dragging = False
        self.flipped = True
        self.colour = colour
        self.num = num
        self.wild = wild
        self.card = card

    def drag(self, surface, increment, hand, network):
        if self.dragging:
            surface.blit(constants.cards[self.card], (self.pos.x + increment.x, self.pos.y + increment.y)) #Blit card based on where the mouse is dragging it
            network.send(f'drag, {hand.cards.index(self)}, ({increment.x},{increment.y})') #Send drag and coords to server

    def card_check(self, card):
        if (self.colour == card.colour and card.colour != 'NA') or (self.num == card.num and self.num != 'NA') or (self.wild == card.wild and card.wild != 'NA') or self.wild in ['ColorChange', 'Draw4'] or card.wild in ['ColorChange', 'Draw4']: #Checks if card can be placed or not based on Uno Rules
            return True
        return False
