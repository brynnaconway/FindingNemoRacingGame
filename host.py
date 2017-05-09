from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys

gs = GameSpace()

# Client Connection
class InitConn(Protocol):
    def connectionMade(self):
        print "Other player has joined."
        reactor.listenTCP(41130, GameHostConnectionFactory())
        self.transport.write("start game")
        
    def dataReceived(self, data):
        pass

class InitConnFactory(ClientFactory):
    def __init__(self):
        self.myConn = InitConn()
    
    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()

class GameHostConnection(Protocol):
    def connectionMade(self):
        print "Created game connection."
        gs.main()
        loop = LoopingCall(gs.loop)
        loop.start(float(1/60)) # like the clock tick

    def dataReceived(self, data):
        print "got data: ", data
        
    
class GameHostConnectionFactory(ClientFactory):
    def __init__(self):
        self.myConn = GameHostConnection()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()

reactor.listenTCP(40130, InitConnFactory())
reactor.run()
