#!/usr/bin/python3

import socket
import numpy
import modules.networkpacking

class server:
  def __init__(self):
    self.gamemap = numpy.array([[False, True, False], [True, False, False]])
    host = "127.0.0.1"
    port = 7897
    self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.serversocket.bind((host, port))

  def main(self):
    self.serversocket.listen()
    clientsocket, addr = serversocket.accept()
    print("accepted connection")
    # array = [0, 1, 3]
    # numarray = numpy.array(array)
    # conn.send(numarray.tobytes())

  def sendmap(self, clientsocket):
    sizebytes = struct.pack(">hh", self.gamemap.shape[0], self.gamemap.shape[1])
    mapbytes = gamemap.tobytes()
    clientsocket.send(sizebytes + mapbytes)

if __name__ == '__main__':
  myserver = server()
  myserver.main()

