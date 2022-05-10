#!/usr/bin/python3

import socket
import numpy
import struct
import random
import selectors
import time

maxnamelength = 16
defaulthost = "127.0.0.1"
bergenchance = 0.05

class networking:
  id: int
  everyonesbergen: bool
  tcplistener: selectors.DefaultSelector
  
  def __init__(self, playername):
    everyonesbergen = random.random() < bergenchance
    host: str = input("Enter the destination ip address " \
        + f"(or blank for {defaulthost}): ")
    if host == "":
      host = defaulthost
    port: int = 7897
    # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sockettcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sockettcp.connect((host, port))
    self.id = struct.unpack('>B', self.sockettcp.recv(1))[0]
    self.tcplistener = selectors.DefaultSelector()
    self.tcplistener.register(self.sockettcp, selectors.EVENT_READ)
    print(self.id)

    playername = playername.encode()
    if len(playername) > 16:
      playername = b'Jeremy Bergen'
    self.sockettcp.send(playername)

    self.sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sockudp.sendto(b'ht', (host, port))

  # def senddata(self, data) -> None:
    # self.sockettcp.send(data.encode)

  def receivemap(self) -> list:
    height, width = struct.unpack(">hh", self.sockettcp\
        .recv(struct.calcsize(">hh")))
    gamemap = numpy.frombuffer(self.sockettcp.recv(width * height), \
        dtype = numpy.bool_)
    gamemap = gamemap.reshape(height, width)
    return gamemap.tolist()

  def playerdata(self, playerclass) -> None:
    pass
    # return dict(players = dict
    # return [[0, "name", [4, 6], [[4, 6], [4, 666], [5, 77]]]]

  def checknewnames(self):
    result = self.tcplistener.select(0)
    if len(result) > 0:
      print(result[0][0].fileobj.recv(maxnamelength + 1))
    
  # def recievesomething(self):
  #   mybuffer = self.sock.recv(1024)
  #   data = numpy.frombuffer(mybuffer, dtype=numpy.uint8)
  #   return data

if __name__ == '__main__':
  mynetworking = networking(input("What's your name?: "))
  print(mynetworking.receivemap())
  while True:
    mynetworking.checknewnames()
    time.sleep(1)
