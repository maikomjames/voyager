#!/usr/bin/python
# coding: utf-8

import sys
import subprocess

COMMANDS = ['help', 'ping', 'whoami']


class Command():
    Name = ['ping', '-c', '15', '-w', '5', '8.8.8.8']

    def __init__(self, socket):
        self.socket = socket

    def run(self):
        p = subprocess.Popen(self.Name, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while (True):
            retcode = p.poll()
            line = p.stdout.readline()
            print (line)
            self.socket.send(line)
            if (retcode is not None):
                break


class whoami(Command):

    Name = ['whoami']


class ping(Command):

    Name = ['ping', '-c', '15', '-w', '5', '8.8.8.8']


class help(Command):

    Name = ['help']