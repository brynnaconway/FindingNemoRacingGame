from myMain import GameSpace
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from twisted.internet.protocol import Factory, Protocol, ClientFactory
import sys

gs = GameSpace()

# Initial Connection 
class InitConn(Protocol):
    def connectionMade(self):
        print "Other player has joined."
        self.transport.write("start game")
        reactor.listenTCP(41130, GameHostConnectionFactory()) # create game connection 
        
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
		gs.main(self.sendData) # open game window 
		try:
			loop = LoopingCall(gs.iteration) # run game program 
			loop.start(float(1/60)) # like the clock tick
			#exit(1)
		except:
			reactor.stop()
			exit(1)

	def dataReceived(self, data):
		gs.get_data(data) # change variables based on data received 

	def sendData(self, data): 
		self.transport.write(data) # send data over connection 
    
class GameHostConnectionFactory(ClientFactory):
    def __init__(self):
        self.myConn = GameHostConnection()

    def buildProtocol(self, addr):
        return self.myConn

    def clientConnectionFailed(self, connector, reason):
        connector.connect()

reactor.listenTCP(40130, InitConnFactory())
reactor.run()
