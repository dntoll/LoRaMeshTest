import sys
import os
cwd = os.getcwd()
sys.path.append(cwd + "\\MeshTestConsole")




from LoRaMeshLibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from LoRaMeshLibrary.Message import Message


def devNullCallback(origin, content):
    #print("Content: " + content)
    return

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = []
views = {}
for i in range(25):
    views[i] = SimTestView(i)
    x = i//5
    y = i%5
    socket = SimulatorSocket(i, x, y, 1.1)
    radio.add(i, socket)
    clients.append(PymeshAdapter(views[i], socket, fpi, devNullCallback))


#All nodes send message to the other side
for i in range(25):
    clients[i].sendMessage(24-i, b"first")

radio.processUntilSilent(secondsOfSilence = 2)

print("Here we should get 24 ACC messages: in " +str(radio.sends) + " sends." )
for i in range(25):

    if views[i].hasMessageFrom(24-i, Message.TYPE_ACC):
        print(str(i) + " got Acc from " + str(24-i))
        
print("ended tests")

fpi.die()
print("tried to release threads")

print()
