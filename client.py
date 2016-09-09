#!/usr/bin/python
# project/server/socket/client.py
# coding: utf-8

import socket
HOST = '127.0.0.1'
PORT = 1234
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

tcp.send('ping')

while True:
    msg_r = tcp.recv(1024)
    if not msg_r:
        break
    print (msg_r)

tcp.close()