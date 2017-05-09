from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys


class GameConnection(Protocol):
    def connectionMade(self):

    def dataReceived(self):

class GameConnectionFactory(ClientFactory):

# Client Connection
class InitClientConn(Protocol):
    def connectionMade(self):

    def dataReceived(self):

class InitClientFactory(ClientFactory):
    def connectionMade(self):

    def dataReceived(self):

