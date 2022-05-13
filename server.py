#!/usr/bin/python3

import numpy
import socket
import struct
import selectors
import random
import sys

from modules import constants

CONNECTION_TCP = 0b01
CONNECTION_SERVERSOCKET = 0b10
CONNECTION_STDIN = 0b100

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
    """
    self.gamemap = numpy.array(
      [
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False, False]
      ]
    )"""
    host = "0.0.0.0"
    port = 7897

    self.freeids = [1]
    self.names = dict()
    self.playerstuff = dict() # playerid:bytes
    
    self.connections = selectors.DefaultSelector()
    # self.connections.register(sys.stdin, selectors.EVENT_READ, \
        # (CONNECTION_STDIN, 0))
    
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
      readyconnections = self.connections.select()
      for readyconnection, __ in readyconnections:
        if readyconnection.data[0] & CONNECTION_STDIN:
          pid = int(input())
          self.sendkill(pid)
        elif readyconnection.data[0] & CONNECTION_TCP:
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
            try:
              data = readyconnection.fileobj.recv(1)
              if data:
                self.sendkill(struct.unpack('>B', data)[0])
              else:
                raise ConnectionResetError
            except ConnectionResetError:
              self.senddisconnect(readyconnection.data[1])
              self.freeids.append(readyconnection.data[1])
              self.names.pop(readyconnection.data[1])
              try:
                self.playerstuff.pop(readyconnection.data[1])
              except KeyError:
                pass
              self.connections.unregister(readyconnection.fileobj)
              readyconnection.fileobj.close()
              
        else:
          playerdata, returnaddress = readyconnection.fileobj.\
              recvfrom(constants.MAXBUFFERSIZE)
          pid = struct.unpack_from('>B', playerdata)[0]
          self.playerstuff[pid] = playerdata
          numplayers = len(self.playerstuff) - 1
          bytestosend = struct.pack('>B', numplayers)
          for key, value in self.playerstuff.items():
            if key != pid:
              bytestosend += value
          readyconnection.fileobj.sendto(bytestosend, returnaddress)
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
          connection.fileobj.send(struct.pack('>BB', constants.NAMEUPDATE, \
              pid) + name)
        else:
          for pair in self.names.items():
            connection.fileobj.send(struct.pack('>BB', constants.NAMEUPDATE, \
                pair[0]) + pair[1])
  
  def sendkill(self, pid):
    for connection in self.connections.get_map().values():
      if connection.data[1] == pid:
        connection.fileobj.send(struct.pack('>B', constants.KILLSIGNAL))

  def senddisconnect(self, pid):
    for connection in self.connections.get_map().values():
      if connection.data[1]:
        connection.fileobj.send(struct.pack('>BB', \
            constants.PLAYERDISCONNECTED, pid))
        
if __name__ == '__main__':
  myserver = server()
  myserver.main()
