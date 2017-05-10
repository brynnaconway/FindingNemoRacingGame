from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys

gs = GameSpace()

# Starting connection before opening game windows 
class InitClientConn(Protocol):
    def connectionMade(self):
        print "Client connection made."
    
    def dataReceived(self, data):
        if data == "start game":
            reactor.connectTCP("localhost", 41130, GameClientConnFactory()) # start game connection 
    
class InitClientConnFactory(ClientFactory):
    def __init__(self):
        self.myConn = InitClientConn()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()
    
class GameClientConn(Protocol):
    def connectionMade(self):
        print "Connected to game host."
        gs.main(self.sendData) # open game window 
        try:
	        loop = LoopingCall(gs.iteration) # run game 
	        loop.start(float(1/60))
        except:
		    exit(1)
    def dataReceived(self, data):
        gs.get_data(data) # use received data in game 

    def sendData(self, data):
    	self.transport.write(data) # send data to other player 

class GameClientConnFactory(ClientFactory):
    def __init__(self):
        self.myConn = GameClientConn()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()    

# Connecting to Host:
reactor.connectTCP("localhost", 40130, InitClientConnFactory())
reactor.run()
