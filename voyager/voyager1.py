#!/usr/bin/python
# coding: utf-8


import socket
import thread
from config import HOST, PORT

from commands import COMMANDS, RunCommand


class Voyager1():

    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        self.last_run = None

        self.command('areyoualive')

        thread.start_new_thread(self.read_anserws, ())

    def read_anserws(self):
        while True:
            msg = self.socket.recv(1024)
            if not msg:
                break
            self.command(msg)

    def command(self, cmd):
        if cmd in COMMANDS:
            run = RunCommand(cmd, self.socket)
            self.last_run = run
        else:
            self.socket.send('%s\n' % 'Command not found.')

    def close(self):
        self.socket.close()

if __name__ == "__main__":
    Voyager1(HOST, PORT)