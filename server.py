from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from time import sleep

#Create the channel to deal with our incoming requests from the client
#A new channel is created every time a client connects
class ClientChannel(Channel):

    #Create a function that will respond to a request to move a player
    def Network_move(self, data):

        #Fetch the data top help us identify which game needs to update
        gameID = data['gameID']
        player = data['player']
        x = data['x']
        y = data['y']

#Create a new server for our game
class GameServer(Server):

    #Set the channel to deal with incoming requests
    channelClass = ClientChannel

    #Constructor to initialize the server objects
    def __init__(self, *args, **kwargs):

        #Call the super constructor
        Server.__init__(self, *args, **kwargs)

        #Create the objects to hold our game ID and list of running games
        self.games = []
        self.queue = None
        self.gameIndex = 0
        
        #Set the velocity of our player
        self.velocity = 5

    #Function to deal with new connections
    def Connected(self, channel, addr):
        print("New connection: {}".format(channel))

        #When we receive a new connection
        #Check whether there is a game waiting in the queue
        if self.queue == None:

            #If there isn't someone queueing
            #Increment the game index
            #Set the game ID for the player channel
            #Add a new game to the queue
            self.gameIndex += 1
            channel.gameID = self.gameIndex
            self.queue = Game(channel, self.gameIndex)

        else:

            #Set the game index for the currently connected channel
            channel.gameID = self.gameIndex

            #Set the second player channel
            self.queue.player_channels.append(channel)

            #Send a message to the clients that the game is starting
            for i in range(0, len(self.queue.player_channels)):
				self.queue.player_channels[i].Send({"action":"startgame","player":i,"gameID":self.queue.gameID,"velocity":self.velocity})

            #Add the game to the end of the game list
            self.games.append(self.queue)

            #Empty the queue ready for the next connection
            self.queue = None

#Create the game class to hold information about any particular game
class Game(object):

    #Constructor
    def __init__(self, player, gameIndex):

        #Create a list of players
        self.players = []
        self.players.append(Player(0, 0))
        self.players.append(Player(0, 550))

        #Store the network channel of the first client
        self.player_channels = [player]

        #Set the game id
        self.gameID = gameIndex
        
#Create a player class to hold all of our information about a single player
class Player(object):
	
	#Constructor
	def __init__(self, x, y):
		
		#Set the x and y
		self.x = x
		self.y = y

#Start the server, but only if the file wasn't imported
if __name__ == "__main__":

    print("Server starting on LOCALHOST...\n")

    #Create a server
    s = GameServer()

    #Pump the server at regular intervals (check for new requests)
    while True:
        s.Pump()
        sleep(0.0001)
