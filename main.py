"""
ICS3U
Omar Toure
This is my final project for this course.
"""

#Import module from project folder
import project.controller as controller


if __name__ == '__main__': #Won't run if code has been imported as a module
    game = controller.GameInstance() #Creates an instance of the class in controller module
    game.run() #Runs the game
