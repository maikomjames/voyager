#!/usr/bin/python
# coding: utf-8


import socket
import thread
from config import HOST, PORT


class Voyager2():

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

        thread.start_new_thread(self.read_anserws, ())

    def read_anserws(self):
        while True:
            msg = self.socket.recv(1024)
            if not msg:
                break
            self.command(msg)

    def command(self, cmd):
        self.socket.send(cmd)

    def sendCommandsAllPeers(self, cmd):
        self.command('Command: %s' % cmd)

    def close(self):
        self.socket.close()

    def input(self):
        msg = raw_input()
        while msg <> '\x18':
            print("enviando: " + msg)
            self.sendCommandsAllPeers(msg)
            msg = raw_input()

if __name__ == "__main__":
    Voyager2(HOST, PORT).input()