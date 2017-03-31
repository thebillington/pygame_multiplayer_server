from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from time import sleep

#Create the channel to deal with our incoming requests from the client
#A new channel is created every time a client connects
class ClientChannel(Channel):

    #Create a function that will respond to every request from the client
    def Network(self, data):

        #Print the contents of the packet
        print(data)

#Create a new server for our game
def GameServer(Server):

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

    #Function to deal with new connections
    def Connected(self, channel, addr):
        print("New connection: {}".format(channel))

#Create the game class to hold information about any particular game
class Game(object):

    #Constructor
    def __init__(self, player0, gameIndex):

        #Set the initial positions of each player
        self.p1x = 0
        self.p1y = 0
        self.p2x = 550
        self.p2y = 0

        #Store the network channel of each client
        self.player0 = player0
        self.player1 = None

        #Set the game id
        self.gameID = gameIndex

#Start the server, but only if the file wasn't imported
if __name__ == "__main__":

    print("Server starting on LOCALHOST...\n")

    #Create a server
    s = GameServer()

    #Pump the server at regular intervals (check for new requests)
    while True:
        s.Pump()
        sleep(0.0001)
