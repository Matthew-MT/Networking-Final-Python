#!/usr/bin/python3

import socket
import numpy
import struct

defaulthost = "127.0.0.1"

class networking:
  def __init__(self):
    host: str = input("Enter the destination ip address " \
        + f"(or blank for {defaulthost}): ")
    if host == "":
      host = defaulthost
    port: int = 7897
    # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sockettcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sockettcp.connect((host, port))

  def senddata(self, data) -> None:
    self.sockettcp.send(data.encode)

  def receivemap(self) -> list:
    height, width = struct.unpack(">hh", self.sockettcp\
        .recv(struct.calcsize(">hh")))
    gamemap = numpy.frombuffer(self.sockettcp.recv(width * height), \
        dtype = numpy.bool_)
    gamemap = gamemap.reshape(height, width)
    return gamemap.tolist()

  def playerdata(self, playrclass) -> list:
    return [[0, "name", [4, 6], [[4, 6], [4, 666], [5, 77]]]]

  # def recievesomething(self):
  #   mybuffer = self.sock.recv(1024)
  #   data = numpy.frombuffer(mybuffer, dtype=numpy.uint8)
  #   return data

if __name__ == '__main__':
  mynetworking = networking()
  print(mynetworking.receivemap())
