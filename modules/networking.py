#!/usr/bin/python3

import socket
import numpy
import struct
import random
import selectors

from modules import constants

defaulthost = "127.0.0.1"

class networking:
  pid: int
  everyonesbergen: bool
  tcplistener: selectors.DefaultSelector
  
  def __init__(self, host = "localhost", playername = 'Jeremy Bergen'):
    self.everyonesbergen = random.random() < constants.UNIVERSAL_PROBABILITY
    self.host: str = host
    if self.host == "":
      self.host = defaulthost
    self.port: int = 7897

    self.sockettcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sockettcp.connect((self.host, self.port))
    self.pid = struct.unpack('>B', self.sockettcp.recv(1))[0]
    self.tcplistener = selectors.DefaultSelector()
    self.tcplistener.register(self.sockettcp, selectors.EVENT_READ)

    playername = playername.encode()
    if len(playername) > constants.MAXNAMELENGTH or len(playername) == 0:
      playername = constants.BERGEN
    else:
      playername = playername.ljust(constants.MAXNAMELENGTH)
    self.sockettcp.send(playername)

    self.sockudp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # self.sockudp.sendto(b'ht', (host, port))

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
    self.checktcpstuff(playerclass)
    bytestosend = struct.pack('>BBhhh', self.pid, len(playerclass.bullets), \
        int(playerclass.pos[0]), int(playerclass.pos[1]), playerclass.score)
    for bullet in playerclass.bullets:
      bytestosend += struct.pack('>hh', int(bullet['pos'][0]), \
          int(bullet['pos'][1]))
    self.sockudp.sendto(bytestosend, (self.host, self.port))
    self.recieveplayerdata(playerclass)
    # return dict(players = dict
    # return [[0, "name", [4, 6], [[4, 6], [4, 666], [5, 77]]]]
    #
  def recieveplayerdata(self, playerclass) -> None:
    playerdata =  self.sockudp.recvfrom(constants.MAXBUFFERSIZE)[0]
    numplayers = struct.unpack_from('>B', playerdata)[0]
    offset = 1
    playerclass.otherBullets = []
    for i in range(numplayers):
      pid, numbullets = struct.unpack_from('>BB', playerdata, offset)
      offset += 2
      position = struct.unpack_from('>hh', playerdata, offset)
      offset += 4
      score = struct.unpack_from('>h', playerdata, offset)[0]
      offset += 2
      try:
        playerclass.otherPlayers[pid]['pos'] = (float(position[0]), \
            float(position[1]))
        playerclass.otherPlayers[pid]['score'] = score
      except KeyError:
        playerclass.otherPlayers[pid] = dict(name = constants.BERGEN, \
            position = (float(position[0]), float(position[1])), \
            score = score)
      bullets = [(0, 0)] * numbullets
      for j in range(numbullets):
        position = struct.unpack_from('>hh', playerdata, offset)
        offset += 4
        bullets[j] = (float(position[0]), float(position[1]))
      playerclass.otherBullets += bullets

  def checktcpstuff(self, playerclass):
    result = self.tcplistener.select(0)
    if len(result) > 0:
      mode = struct.unpack('>B', result[0][0].fileobj.recv(1))[0]
      if mode == constants.NAMEUPDATE:
        pid = struct.unpack('>B', result[0][0].fileobj.recv(1))[0]
        name = result[0][0].fileobj.recv(constants.MAXNAMELENGTH).decode().strip()
        if self.everyonesbergen:
          name = constants.BERGEN
        playerclass.otherPlayers[pid] = dict(name = name)
      elif mode == constants.KILLSIGNAL:
        playerclass.respawn()
      elif mode == constants.PLAYERDISCONNECTED:
        pid = struct.unpack('>B', result[0][0].fileobj.recv(1))[0]
        playerclass.otherPlayers.pop(pid)
        playerclass.respawn()

  def sendkillsignal(self, playerid):
    self.sockettcp.send(struct.pack(">B", playerid))
    
  # def recievesomething(self):
  #   mybuffer = self.sock.recv(1024)
  #   data = numpy.frombuffer(mybuffer, dtype=numpy.uint8)
  #   return data
