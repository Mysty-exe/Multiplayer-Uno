#Import required modules
import pygame

#Initialize Pygame sound module
pygame.mixer.pre_init()
pygame.mixer.init()

class Sound():
    """Represents a Sound object"""

    def __init__(self):
        #Load up the sounds that will play
        pygame.mixer.music.load('audio/bg.mp3')
        self.transition = pygame.mixer.Sound('audio/transition.wav')

        #Loops the background music and sets the volume
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(loops=-1)  

        #Sets the volume for the transition
        self.transition.set_volume(0.3)

    def self_transition(self):
        """Plays transition sound"""
        pygame.mixer.Channel(0).play(self.transition) #Plays the transition sound on a different channel
