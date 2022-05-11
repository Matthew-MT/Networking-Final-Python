#!/usr/bin/python3

import numpy
import socket
import struct
import selectors
import random

from modules import constants

CONNECTION_TCP = 0b01
CONNECTION_SERVERSOCKET = 0b10

class server:
  def __init__(self):
    self.gamemap = numpy.array(
      [
        [False, True , False, False, True , True , False, True , False, False, False, False],
        [False, False, True , False, False, False, False, True , False, False, True , True ],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, True , False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, True , True , True , False, False, False, False, False, False, False, False]
      ]
    )
    host = "0.0.0.0"
    port = 7897

    self.freeids = [0]
    self.names = {}
    
    self.connections = selectors.DefaultSelector()
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen()
    self.connections.register(serversocket, selectors.EVENT_READ, \
        (CONNECTION_TCP | CONNECTION_SERVERSOCKET, 0))
    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serversocket.bind((host, port))
    self.connections.register(serversocket, selectors.EVENT_READ, \
        (CONNECTION_SERVERSOCKET, 0))
    # print(serversocket.recvfrom(2))

  def main(self):
    while True:
      print('selecting...')
      readyconnections = self.connections.select()
      for readyconnection, __ in readyconnections:
        if readyconnection.data[0] & CONNECTION_TCP:
          if readyconnection.data[0] & CONNECTION_SERVERSOCKET:
            clientsocket = readyconnection.fileobj.accept()[0]
            pid = self.freeids.pop()
            if len(self.freeids) == 0:
              self.freeids.append(pid + 1)
            self.connections.register(clientsocket, selectors.EVENT_READ, \
                (CONNECTION_TCP, pid))
            clientsocket.send(struct.pack('>B', pid))
            name = clientsocket.recv(constants.MAXNAMELENGTH)
            if random.random() < constants.UNIVERSAL_PROBABILITY:
              name = constants.BERGEN
            self.sendmap(clientsocket)
            self.sendnames(pid, name)
            self.names[pid] = name
          else:
            data = readyconnection.fileobj.recv(2)
            if data:
              print(data)
            else:
              self.freeids.append(readyconnection.data[1])
              self.names.pop(readyconnection.data[1])
              self.connections.unregister(readyconnection.fileobj)
              readyconnection.fileobj.close()
        else:
          print(readyconnection.fileobj.recvfrom(2))
    # array = [0, 1, 3]
    # numarray = numpy.array(array)
    # conn.send(numarray.tobytes())

  def sendmap(self, clientsockettcp):
    sizebytes = struct.pack(">hh", self.gamemap.shape[0], self.gamemap.shape[1])
    mapbytes = self.gamemap.tobytes()
    clientsockettcp.send(sizebytes + mapbytes)

  def sendnames(self, pid, name):
    for connection in self.connections.get_map().values():
      if connection.data[0] == CONNECTION_TCP: # bad code
        if connection.data[1] != pid:
          connection.fileobj.send(struct.pack('>B', pid) + name)
        else:
          print(self.names)
          for pair in self.names.items():
            connection.fileobj.send(struct.pack('>B', pair[0]) + pair[1])
        
if __name__ == '__main__':
  myserver = server()
  myserver.main()
  myserver.sendmap(myserver.aclientsockettcp)
