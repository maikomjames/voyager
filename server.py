#!/usr/bin/python
# project/server/socket/server.py
# coding: utf-8

import socket
import thread
from commands import COMMANDS, help, ping, whoami


HOST = '127.0.0.1'
PORT = 1234


class Voyager1():

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.clients = []

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.conn.bind(tuple([host, port]))
        self.conn.listen(1)

        while True:
            con, cliente = self.conn.accept()
            thread.start_new_thread(self.process_client_message, tuple([con, cliente]))

    def process_client_message(self, con, cliente):
        while True:
            msg = con.recv(1024)
            if not msg: break
            self.add_clients(cliente)
            print ("Recebi: %s" % msg)
            self.command(msg, con)

        con.close()
        thread.exit()

    def command(self, cmd, con):
        if cmd in COMMANDS:
            globals()[cmd](con).run()

    def add_clients(self, client_identify):
        for cl in self.clients:
            if cl == client_identify:
                return
        self.clients.append(client_identify)

    def __del__(self):
        self.conn.close()


if __name__ == "__main__":
    Voyager1(HOST, PORT)
