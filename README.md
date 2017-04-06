# pygame_multiplayer_server

This program is a very basic implementation of the PodSixNet server library using Pygame. There are two main components of the server, which are the client (game.py) and the server (server.py)

###Client

The client is a PodSixNet ConnectionListener which can pump a connected server for new packets at regular time intervals. The OnlineGame class implements the ConnectionListener as well as all of the necessary pygame components to make the game run.

Each client has a player number and game ID, which is received from the server when the *startgame* message is received. This is used to identify which player is moving their character (when the request is sent to the server).

There is also a *position* network function, used to move the other player when a message is received from the server, notifying the client that the other player has moved.

###Server

The server is a combination of a PodSixNet Server and Channel. The Server deals with sending messages to the clients, as well as new connections and game logic. The server has a field *channelClass* which points it to a Channel object, used to receive requests from the user and pass them on to the server.

When the server receives a connection from a new player, it checks the queue to see if there is a player already waiting. If there isn't, it creates a new game object and stores the players channel so that data can be sent back to the correct client.

If there is already a player in a queue, the second client Channel is added to the game object, and the startgame message is sent to both clients, allowing the game to load and notifying the client of the gameID and which player they are.

##Improvements

The PodSixNet server uses TCP rather than UDP, making the sending of packets a costly process. In my original build of this test game, whenever a player was moved there was a message sent to both clients informing them of both player positions.

To improve the efficiency of the server the code has now been changed, so that a message is only sent to the player that DIDN'T move, and updates for this player moving are handled client side. This potentially would open room for cheating, however since any game physics (none so far) would be implemented on the server side, this wouldn't matter too much.

The PodSixNet server is ideal for writing turn based games, however it isn't so good for writing games that require a high number of regular updates, so bear this in mind when writing your server.
