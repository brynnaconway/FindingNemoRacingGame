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
            reactor.connectTCP("newt.campus.nd.edu", 41130, GameClientConnFactory())
    
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
        gs.main()
        loop = LoopingCall(gs.iteration)
        loop.start(float(1/60))
    
    def dataReceived(self, data):
        print "got data: ", data

class GameClientConnFactory(ClientFactory):
    def __init__(self):
        self.myConn = GameClientConn()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()    

# Connecting to Host:
reactor.connectTCP("newt.campus.nd.edu", 40130, InitClientConnFactory())
reactor.run()
