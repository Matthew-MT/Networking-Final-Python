#!/usr/bin/python3

import numpy
import socket
import struct
import selectors

CONNECTION_TCP = 0b01
CONNECTION_SERVERSOCKET = 0b10

class server:
  def __init__(self):
    self.gamemap = numpy.array([[False, True, False], [True, False, False]])
    host = "0.0.0.0"
    port = 7897
    # self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.serversockettcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversockettcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serversockettcp.bind((host, port))

  def main(self):
    self.serversockettcp.listen()
    connections = selectors.DefaultSelector()
    connections.register(self.serversockettcp, selectors.EVENT_READ, \
        CONNECTION_TCP | CONNECTION_SERVERSOCKET)
    while True:
      print('selecting...')
      readyconnections = connections.select()
      for readyconnection, __ in readyconnections:
        if readyconnection.data & CONNECTION_SERVERSOCKET:
          clientsocket = readyconnection.fileobj.accept()[0]
          connections.register(clientsocket, selectors.EVENT_READ, \
              readyconnection.data & CONNECTION_TCP)
        else:
          data = readyconnection.fileobj.recv(2)
          if data:
            print(data)
          else:
            connections.unregister(readyconnection.fileobj)
            readyconnection.fileobj.close()
    # array = [0, 1, 3]
    # numarray = numpy.array(array)
    # conn.send(numarray.tobytes())

  def sendmap(self, clientsockettcp):
    sizebytes = struct.pack(">hh", self.gamemap.shape[0], self.gamemap.shape[1])
    mapbytes = self.gamemap.tobytes()
    clientsockettcp.send(sizebytes + mapbytes)

if __name__ == '__main__':
  myserver = server()
  myserver.main()
  myserver.sendmap(myserver.aclientsockettcp)
