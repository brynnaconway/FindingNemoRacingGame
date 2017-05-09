from game import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys

class InitClientConn(Protocol):
    def connectionMade(self):
        print "Client connection made."
    
    def dataReceived(self, data):
        print "Client Init got data: ", data
    
class InitClientConnFactory(ClientFactory):
    def __init__(self):
        self.myConn = InitClientConn()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()
    
#class GameClientConn(Protocol):
    
#class GameClientConnFactory(ClientFactory):

# Connecting to Host:
reactor.connectTCP("newt.campus.nd.edu", 40130, InitClientConnFactory())
reactor.run()
