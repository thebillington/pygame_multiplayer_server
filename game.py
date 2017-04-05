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
        self.players = []
        self.players.append(Player(pygame.image.load("player1.png")))
        self.players.append(Player(pygame.image.load("player2.png")))
        self.players[1].rect.x = width - self.players[1].rect.width
        
        #Initialize the gameID and player ID
        self.gameID = None
        self.player = None

        #Create the game clock
        self.clock = pygame.time.Clock()
        
        #Fill the screen with our background colour
        self.screen.fill(self.bg)

        #Connect to the server
        self.Connect()
        
        #Set running to false
        self.running = False
        
        #While the game isn't running pump the server
        while not self.running:
			#Check if the user exited the game
			self.check_exit()
			
			self.Pump()
			connection.Pump()
			sleep(0.01)	

        #Update the caption
        pygame.display.set_caption("Game ID: {} - Player: {}".format(self.gameID, self.player))
        
    #Create a function to tell the server what keys are being pressed
    def check_keys(self):
		
		#Get the keys that are being pressed
		keys = pygame.key.get_pressed()
		
		#Check which keys were pressed
		if keys[K_UP]:
			#Send the server an update
			self.Send({"action":"move","key":"UP","player":self.player,"gameID":self.gameID})
		if keys[K_DOWN]:
			#Send the server an update
			self.Send({"action":"move","key":"DOWN","player":self.player,"gameID":self.gameID})
		if keys[K_LEFT]:
			#Send the server an update
			self.Send({"action":"move","key":"LEFT","player":self.player,"gameID":self.gameID})
		if keys[K_RIGHT]:
			#Send the server an update
			self.Send({"action":"move","key":"RIGHT","player":self.player,"gameID":self.gameID})

    #Create the function to update the game
    def update(self):

        #Pump the server to check for updates
        connection.Pump()
        self.Pump()

        #Check if the user exited
        self.check_exit()
        
        #Check if any keys were being pressed
        self.check_keys()

        #Tick the game clock
        self.clock.tick(60)

        #Fill the background
        self.screen.fill(self.bg)

        #Draw the players
        for p in self.players:
			self.screen.blit(p.img, p.rect)

        #Update the display
        pygame.display.flip()

    #Create a function to receive the start game signal
    def Network_startgame(self, data):
		#Get the game ID and player number from the data
		self.gameID = data['gameID']
		self.player = data['player']
		#Set the game to running so that we enter the update loop
		self.running = True
        
    #Create a function that lets us check whether the user has clicked to exit (required to avoid crash)
    def check_exit(self):
		#Check if the user exited
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				#exit()
				
#Create a class to hold our character information
class Player(object):
	
	#Constructor
	def __init__(self, img):
		
		#Set our object fields
		self.img = img
		self.rect = img.get_rect()

#If the file was run and not imported
if __name__ == "__main__":

    #Create the game object
    og = OnlineGame()

    #Every tick update the game
    while True:
        og.update()
