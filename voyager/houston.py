#!/usr/bin/python
# coding: utf-8

from time import sleep
import socket
import sys
import thread
from config import HOST, PORT
import re
from datetime import datetime


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
            try:
                con, cliente = self.conn.accept()
                thread.start_new_thread(self.process_client_message, tuple([con, cliente]))
            except Exception as e:
                pass

    def process_client_message(self, con, cliente):
        while True:
            msg = con.recv(1024)
            if not msg:
                break
            m = re.search('Command:\s(.*)', msg)
            self.print_messages("%s: %s" % (cliente, msg))
            if m:
                self.sendCommandAllPeer(m.group(1))
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

    def listen(self):
        while True:
            pass

    def print_messages(self, msg):
        print ("%s - %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg))

    def __del__(self):
        self.conn.close()
        sys.exit(0)


if __name__ == "__main__":
    houston = Houston(HOST, PORT)
    houston.listen()
