#!/usr/bin/python3

import socket
import numpy
import struct
import modules.networkpacking

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
    self.aclientsockettcp, addr = self.serversockettcp.accept()
    print("accepted connection, sending map")
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
