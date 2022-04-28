#!/usr/bin/python3

import socket
import numpy

class Networking:
  def __init__(self):
    host = "127.0.0.1"
    port = 7897
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    print("__init__ done")

  def senddata(self, data) -> None:
    self.sock.send(data.encode)

  def recievedata(self):
    mybuffer = self.sock.recv(1024)
    data = numpy.frombuffer(mybuffer, dtype=numpy.uint8)
    return(data)

if __name__ == '__main__':
  networking = Networking()
  print(networking.recievedata())
