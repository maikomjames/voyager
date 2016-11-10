#!/usr/bin/python
# coding: utf-8


import SocketServer
import threading


class HoustonThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.server.add_client((self.client_address, self.request))

        self.data = self.request.recv(1024).strip()
        self.server.last_message_sent = self.data
        print "Recebi server: {}".format(self.data)
        # print "{} wrote:".format(self.client_address[0])
        # print self.data
        # just send back the same data, but upper-cased
        self.server.envia_mensage(self.data)


class HoustonThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, *args, **kws):
        self.clients = []
        self.last_message_sent = None
        SocketServer.TCPServer.__init__(self, *args, **kws)

    def add_client(self, client):
        self.clients.append(client)

    def get_last_message_sent(self):
        return self.last_message_sent

    def envia_mensage(self, message):
        for client_data in self.clients:
            client, request = client_data
            request.sendall(message)


class Houston:

    def __init__(self, config):
        self.config = config
        self.server = None
        self.server_thread = None

    def listen(self):

        # Create the server
        self.server = HoustonThreadedTCPServer(self.config, HoustonThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def close(self):
        self.server.shutdown()
        self.server.server_close()

    def count_clients(self):
        return len(self.server.clients)

    def get_last_message_sent(self):
        return self.server.last_message_sent


# if __name__ == "__main__":
#     Houston(HOST, PORT)
