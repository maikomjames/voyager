#!/usr/bin/python
# project/server/socket/client.py
# coding: utf-8

import socket
import thread
HOST = '0.0.0.0'
PORT = 1234
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)


def process_client_message(test):
    while True:
        r = tcp.recv(1024)
        if not r:
            break
        if r == 'yes, I am ;)\n':
            tcp.send("areyoualive")
        print (r)


msg = raw_input()
while msg <> '\x18':
    tcp.send(msg)
    thread.start_new_thread(process_client_message, tuple(['a']))
    msg = raw_input()

thread.exit()
tcp.close()