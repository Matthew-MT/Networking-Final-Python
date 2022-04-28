#!/usr/bin/python3

import socket
import numpy

def main():
  gamemap = [[False, True, False], [True, False, False]]
  host = "127.0.0.1"
  port = 7897
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((host, port))
    serversocket.listen()
    conn, addr = serversocket.accept()
    print("accepted connection")
    array = [0, 1, 3]
    numarray = numpy.array(array)
    conn.send(numarray.tobytes())

main()

