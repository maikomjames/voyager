#!/usr/bin/python
# coding: utf-8


import socket
import thread

from commands import COMMANDS, RunCommand

HOST = '0.0.0.0'
PORT = 1234


class Voyager1():

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.socket.send('areyoualive')

        self.read_anserws('a')

    def read_anserws(self, a):
        while True:
            msg = self.socket.recv(1024)
            if not msg:
                break
            thread.start_new_thread(self.command, (msg, self.socket))

    def command(self, cmd, con):
        if cmd in COMMANDS:
            RunCommand(cmd, con)
        # else:
            #con.send('%s\n' % 'Command not found.')


if __name__ == "__main__":
    Voyager1(HOST, PORT)