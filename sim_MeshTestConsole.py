from msilib.schema import Component
import threading



from LoRaMeshLibrary.PymeshAdapter import PymeshAdapter
from simulator.SimulatorSocket import SimulatorSocket
from simulator.FakePycomInterface import FakePycomInterface
from simulator.Radio import Radio
from simulator.SimTestView import SimTestView
from simulator.FakePycomInterface import FakePycomInterface

from LoRaMeshLibrary.Message import Message
from LoRaMeshLoPyConsole.view.SerialConsoleView import SerialConsoleView
from LoRaMeshLoPyConsole.view.CompositeView import CompositeView
from LoRaMeshLoPyConsole.MeshTestConsole import MeshTestConsole
from time import sleep

radio = Radio()
fpi = FakePycomInterface()

y = 0
clients = {}
views = {}

def devNullCallback(origin, content):
    #print("Content: " + content)
    return

for i in range(25):
    views[i] = CompositeView()
    nodeCallBack = devNullCallback
    if i == 0:
        views[i] = SerialConsoleView()
        nodeCallBack = MeshTestConsole.callback
    x = i//5
    y = i%5
    socket = SimulatorSocket(i, x, y, 1.5)
    radio.add(i, socket)
    clients[i] = PymeshAdapter(views[i], socket, fpi, nodeCallBack)



c = MeshTestConsole(views[0], FakePycomInterface(), clients[0])
c.run()

def radioThreadFunc(radio, c):
    while True:
        radio.process()
        sleep(0.5)
        print(end="", flush=True)

t = threading.Thread(target=radioThreadFunc, args=(radio, c), daemon=True)
t.start() 


while True:
    sleep(0.1)
    ch = input("Input command master [#] Send from 0 to # node ID, [Q]uit], [S]:")
    if ch:
        if ch.isnumeric():
            clients[0].sendMessage(int(ch), b"Message")
        elif ch == "P":
            clients[0].pingNeighbors()
        elif ch == "P1":
            clients[1].pingNeighbors()
        elif ch == "Q":
            break
        elif ch == "S":
            s = input("Input Sender #:")
            t = input("Input Target #:")
            m = input("Input Message :")
            clients[int(s)].sendMessage(int(t), m.encode('utf-8'))
            
