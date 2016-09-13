#!/usr/bin/python
# coding: utf-8

import signal
import socket
import sys
import thread
from config import HOST, PORT


class Houston():

    def __init__(self, host, port):
        self.host = host
        self.port = port

        self.clients = []

        # signal.signal(signal.SIGINT, self.signal_handler)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.conn.bind(tuple([host, port]))
        self.conn.listen(1)

        thread.start_new_thread(self.read_clientes, tuple())

    def read_clientes(self):
        while True:
            con, cliente = self.conn.accept()
            thread.start_new_thread(self.process_client_message, tuple([con, cliente]))

    def process_client_message(self, con, cliente):
        while True:
            msg = con.recv(1024)
            if not msg:
                break
            self.add_clients(con, cliente)

        con.close()
        thread.exit()

    def close(self):
        self.conn.close()

    def command(self, cmd, con):
        try:
            con.send(cmd)
        except Exception as e:
            self.remove_cliente(con)
            print ("Error! Client desconectado!")

    def add_clients(self, con, client_identify):
        for cl in self.clients:
            if cl[1] == client_identify:
                return

        self.clients.append((con, client_identify))

    def remove_cliente(self, con):
        for cl in self.clients:
            if cl[0] == con:
                self.clients.remove(cl)
                return

    def sendCommandAllPeer(self, cmd):
        for cl in self.clients:
            self.command(cmd, cl[0])

    def input(self):
        msg = raw_input()
        while msg <> '\x18':
            self.sendCommandAllPeer(msg)
            msg = raw_input()

    def signal_handler(self, signal, frame):
        self.conn.close()
        sys.exit(0)

    def __del__(self):
        self.conn.close()
        sys.exit(0)


if __name__ == "__main__":
    Houston(HOST, PORT)
