from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys

gs = GameSpace()

class InitClientConn(Protocol):
    def connectionMade(self):
        print "Client connection made."
    
    def dataReceived(self, data):
        if data == "start game":
            reactor.connectTCP("localhost", 41130, GameClientConnFactory())
    
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
        gs.main(self.sendData)
        try:
	        loop = LoopingCall(gs.iteration)
	        loop.start(float(1/60))
        except:
		    exit(1)
    
    def dataReceived(self, data):
        gs.get_data(data)

    def sendData(self, data):
    	self.transport.write(data)

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
