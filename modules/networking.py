#!/usr/bin/python3

import socket
import numpy
import struct

class networking:
  def __init__(self):
    host: str = input("Enter the destination ip address " \
        + "(or blank for 127.0.0.1):")
    if host == "":
      host = "127.0.0.1"
    port: int = 7897
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))
    print("__init__ done")

  def senddata(self, data) -> None:
    self.sock.send(data.encode)

  def receivemap(self) -> list:
    height, width = struct.unpack(">hh", self.sock.recv(struct.calcsize(">hh")))
    gamemap = numpy.frombuffer(self.sock.recv(width * height), \
        dtype = numpy.bool_)
    gamemap = gamemap.reshape(height, width)
    return gamemap.tolist()

  # def recievesomething(self):
  #   mybuffer = self.sock.recv(1024)
  #   data = numpy.frombuffer(mybuffer, dtype=numpy.uint8)
  #   return data

if __name__ == '__main__':
  mynetworking = networking()
  print(mynetworking.receivemap())
