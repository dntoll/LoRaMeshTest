from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from LoRaMeshLoPyConsole.view.CompositeView import CompositeView

from simulator.SimulatorSocket import SimulatorSocket
from LoRaMeshLibrary.PymeshAdapter import PymeshAdapter
from LoRaMeshLibrary.Message import Message
from time import sleep

class SimTest:
    def __init__(self, showOutput = False):
        self.radio = Radio()
        self.fpi = FakePycomInterface()
        
        self.views = {}
        self.clients = {}
        self.showOutput = showOutput

    def callBack(nodeID, MessageBytes):
        print(MessageBytes)

    def add(self, nodeId, x, y):
        socket = SimulatorSocket(nodeId, x, y, 1.1)
        self.radio.add(nodeId, socket)
        self.views[nodeId] = SimTestView(nodeId)
        
        self.clients[nodeId] = PymeshAdapter(self.views[nodeId], socket, self.fpi, SimTest.callBack)

    def disableRadio(self, nodeId):
        self.radio.disableRadio(nodeId)
    
    def clearMessages(self, nodeId):
        self.views[nodeId].clearMessages()


    def send(self, fromNodeID, to, message):
        self.clients[fromNodeID].sendMessage(to, message)
    
    def ping(self, fromNodeID):
        self.clients[fromNodeID].pingNeighbors()

    def endSim(self):
        self.fpi.die()

    def processUntilSilent(self, secondsOfSilence):
        self.radio.processUntilSilent(secondsOfSilence)
        print("process until silent")

    def assertHasMessage(self, nodeID, messageType):
        if messageType == Message.TYPE_ACC:
            t = "acc"
        elif messageType == Message.TYPE_FIND:
            t = "find"
        elif messageType == Message.TYPE_PING:
            t = "ping"
        else:
            t = "message"
        hasMess = self.views[nodeID].hasMessage(messageType)

        assert hasMess, "No message on node " + str(nodeID) + " of type " + t
    
    def assertHasNoMessage(self, nodeID, messageType):
        if messageType == Message.TYPE_ACC:
            t = "acc"
        elif messageType == Message.TYPE_FIND:
            t = "find"
        elif messageType == Message.TYPE_PING:
            t = "ping"
        else:
            t = "message"

        hasMess = self.views[nodeID].hasMessage(messageType)

        assert not hasMess, "No message on node " + str(nodeID) + " of type " + t
        
