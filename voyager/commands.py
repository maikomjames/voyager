#!/usr/bin/python
# coding: utf-8

import sys
import subprocess

COMMANDS = ['help', 'ping', 'whoami', 'areyoualive', 'listsocketclients']


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
            self.socket.send(self.print_line(line))
            if (retcode is not None):
                break

    def print_line(self, str):
        return '%s\n' % str


class RunCommand():
    def __init__(self, cmd, con):
        globals()[cmd](con).run()


class whoami(Command):

    Name = ['whoami']


class ping(Command):

    Name = ['ping', '-c', '20', '-w', '20', '8.8.8.8']


class help(Command):

    Name = ['help']

    def run(self):
        for command in COMMANDS:
            self.socket.send(self.print_line(command))


class areyoualive(Command):

    Name = ['areyoualive']

    def run(self):
        self.socket.send(self.print_line('yes, I am ;)'))


