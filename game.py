import pygame

from PodSixNet.Connection import ConnectionListener, connection

from time import sleep

from pygame.locals import *

#Create a new class to hold our game object
#This extends the connection listener so that we can pump the server for messages
class OnlineGame(ConnectionListener):

    #Constructor
    def __init__(self):

        #Initialize the game
        pygame.init()
        size = width, height = 600, 600
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Online Game")

        #Set the background colour
        self.bg = (200, 200, 200)

        #Create the players
        self.p1 = pygame.image.load("player1.png")
        self.p2 = pygame.image.load("player2.png")
        self.p1_rect = self.p1.get_rect()
        self.p2_rect = self.p2.get_rect()
        self.p2_rect.x = width - self.p2_rect.width

        #Create the game clock
        self.clock = pygame.time.Clock()

        #Connect to the server
        self.Connect()

    #Create the function to update the game
    def update(self):

        #Pump the server to check for updates
        connection.Pump()
        self.Pump()

        #Check if the user exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #exit()

        #Tick the game clock
        self.clock.tick(60)

        #Fill the background
        self.screen.fill(self.bg)

        #Draw the players
        self.screen.blit(self.p1, self.p1_rect)
        self.screen.blit(self.p2, self.p2_rect)

        #Update the display
        pygame.display.flip()

    #Create a function to receive the start game signal
    def Network_startgame(self, data):
        print(data)

#If the file was run and not imported
if __name__ == "__main__":

    #Create the game object
    og = OnlineGame()

    #Every tick update the game
    while True:
        og.update()
