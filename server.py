#Import required modules
import socket
import pickle
from _thread import *
from project.game import Game
from project.math import Vector
import project.constants as constants

game = None #Game object
HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates a server
s.bind((HOST, PORT)) #Binds server to a certain host and port so clients can connect to it
s.listen(2) #Server listens for clients
num_of_players = 0 #Number of players connected

def parse(hand, card, coord):
    """
	Takes a string and parses it to get a coord
	Args:
		card (number)
		coord (str)
	Returns:
		(object)
        Vector Object
	"""

    minimum, maximum = hand.current_cards() #Get current card indexes on screen

    try:
        x = []
        y = []
        main = x #put number in x list
        for char in coord:
            if char.isdigit() or char == '-': #Check if the character is a number or a negative sign
                main.append(char) #Add it to x or y
            if char == ',': #Check if the charachter is a comma
                main = y #switch from x to y
        
        x, y = int(''.join(x)), int(''.join(y)) #Split list into numbers
        if y == 590:
            x = constants.HAND_COORDS[len(hand.cards[minimum:maximum]) - 1] + (75 * hand.cards.index(card)) #Get card x-coord
        coord = Vector(x, y)
        return coord
    except Exception as e:
        print(e)

def threaded(conn, player):
    """
	Multithreaded function that makes sure client can communicate with each other
	Args:
		conn (object)
		player (int)
	Returns:
		(None)
	"""

    global game, num_of_players

    while True:
        try:
            data = conn.recv(4096).decode() #Receive data from the client and decode it

            if not data: #Check if there is no data
                game = None
                break #Disconnect
            
            hand = None
            if player == 1:
                hand = game.hand1
            else:
                hand = game.hand2

            data = data.split(', ') #Split data into a list
            type1 = data[0]
            type2 = data[1]
            type3 = data[2]

            if type1 == 'Won':
                game.won = player #Set the game winner
                break

            elif type1 == 'disconnect':
                break #Disconnect

            elif type1 == 'draw':
                card = game.draw_deck.cards.pop() #Remove the top card from the draw deck
                hand.cards.append(card) #Put the card in your hand
                hand.reformat_hand()
                if game.turn == 1:
                    game.turn = 2
                else:
                    game.turn = 1

            elif type1 == 'start-dragging':
                hand.cards[int(type2)].dragging = True #Make that card start dragging

            elif type1 == 'stop-dragging':
                try:
                    hand.cards[int(type2)].dragging = False #Make that card stop dragging
                except Exception as e:
                    pass

            elif type1 == 'reset-card':
                type3 = parse(hand, hand.cards[int(type2)], type3) #Parse coord
                hand.cards[int(type2)].pos = type3 #Set the coord
                hand.cards[int(type2)].dragging = False #Stop dragging

            elif type1 == 'drag':
                try:
                    type3 = parse(hand, hand.cards[int(type2)], type3) #Parse the coord
                    hand.cards[int(type2)].pos += type3 #Add increment to card
                except Exception as e:
                    print(e)
                    pass

            elif type1 == 'drag-to-pile':
                try:
                    card = hand.cards[int(type2)]
                    game.pile.cards.append(card) #Add card to pile
                    hand.cards.remove(card) #Remove card from hand 
                    card.dragging = False #Stop dragging
                    card.pos = game.pile.pos #Set coord to pile coord
                    hand.reformat_hand() #Reformat the hand
                    if card.wild != 'Wild1' and card.wild != 'ColorChange':
                        if game.turn == 1:
                            game.turn = 2
                        else:
                            game.turn = 1

                    # Set num variable to loop if it's a draw 2 or draw 4
                    num = 0
                    draw = False
                    if card.wild == 'Draw2':
                        draw = True
                        num = 2
                    elif card.wild == 'Draw4':
                        draw = True
                        num = 4

                    #Loop if it's a draw card
                    if draw:
                        h = None
                        if player == 1:
                            h = game.hand2
                        else:
                            h = game.hand1
                        for _ in range(num):
                            card = game.draw_deck.cards.pop()
                            h.cards.append(card)
                        h.reformat_hand()

                except Exception as e:
                    print(e)

            elif type1 == 'change-r':
                hand.num += 1 #Change card slider
                hand.reformat_hand() #Reformat hand

            elif type1 == 'change-l':
                hand.num -= 1 #Change card slider
                hand.reformat_hand() #Reformat hand

            elif type1 == 'reset_deck':
                for card in game.pile.cards[:-1]:  #Loop through pile
                    card.pos = game.draw_deck.pos #Change card coord to draw deck coord
                    card.flipped = True #Flip card
                    game.pile.cards.remove(card) #Remove card in pile
                    game.draw_deck.cards.append(card) #Put the card in draw deck

            elif type1 == 'get':
                game.current_player = player #Check who the current player is and update it
                conn.sendall(pickle.dumps(game)) #Send gnme object back to client

            if game == None:
                continue

            if player == 1:
                game.hand1 = hand
            else:
                game.hand2 = hand

        except Exception as e:
            print(e)
            game = None
            break

    print('Disconnected')
    num_of_players -= 1
    conn.close() #Close connection


while True:
    conn, addr = s.accept() #Accepts a client
    if num_of_players < 2:
        num_of_players += 1 #Adds a player
        conn.send('Not Full'.encode())
    else:
        conn.send('Full'.encode())
        conn.close()
        continue
    p = 1 #Player one

    if num_of_players == 2: #Runs if player 2 joined and the game is ready to start
        game.ready = True #Both player 1 and 2 are ready
        game.hand2.reformat_hand() #Reformats the hand of player 2
        p = 2 #Player 2
    else: #Runs if player 1 joined and is waiting for player 2
        game = Game() #Creates the game object
        game.hand1.reformat_hand() #Reformats the hand of player 1

    # conn.sendall(pickle.dumps(game)) #Serializes the game object into bytes and sends it over to the client
    start_new_thread(threaded, (conn, p)) #Starts a thread so the server can handle both clients asynchronously (at the same time)

s.close() #Closes the connection
