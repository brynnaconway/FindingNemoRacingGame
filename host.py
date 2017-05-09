from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys


#class GameHostConnection(Protocol):

#class GameHostConnectionFactory(ClientFactory):


# Client Connection
class InitConn(Protocol):
    def connectionMade(self):
        print "Other player has joined."
        self.transport.write("start game")
        #reactor.listenTCP(42130, GameHostConnectionFactory())

    def dataReceived(self, data):
        print "Init host got data: ", data

class InitConnFactory(ClientFactory):
    def connectionMade(self):
        self.myConn = InitConn()
    
    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()

reactor.listenTCP(40130, InitConnFactory())
reactor.run()
