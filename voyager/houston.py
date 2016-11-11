#!/usr/bin/python
# coding: utf-8


import SocketServer
import threading
import re


class HoustonListClients:
    def __init__(self, *args, **kws):
        self.clients = []

    def add_client(self, request, address):
        self.clients.append(HoustonClientRequest(client_address=address, request=request))

    def get_clients(self):
        return self.clients

    def get_total_clients(self):
        return len(self.clients)

    def sendall(self, message):
        for cli in self.clients:
            if not cli.is_mission_control:
                cli.request.sendall(message)

    def get_client(self, address):
        for cli in self.clients:
            if cli.client_address == address:
                return cli
        return None

    def set_as_mission(self, address):
        cli = self.get_client(address)
        cli.is_mission_control = True


class HoustonClientRequest:
    def __init__(self, *args, **kws):
        self.client_address = kws.get('client_address')
        self.request = kws.get('request')
        self.is_mission_control = kws.get('is_mission_control', False)


class HoustonThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def handle(self):

        self.data = self.request.recv(1024).strip()
        print("Houston recebeu: {}".format(self.data))
        r = re.search('Mission\ssad\:?\s(.*)', self.data)
        if r:
            self.server.clients.set_as_mission(self.client_address)
            self.server.last_message_sent = r.group(1)
            self.server.clients.sendall(r.group(1))


class HoustonThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):

    def __init__(self, *args, **kws):
        self.clients = HoustonListClients()
        self.last_message_sent = None
        SocketServer.TCPServer.__init__(self, *args, **kws)

    def get_last_message_sent(self):
        return self.last_message_sent

    def process_request(self, *args, **kws):
        self.clients.add_client(*args)
        SocketServer.ThreadingMixIn.process_request(self, *args, **kws)

    # def process_request_thread(self, *args, **kws):
    #     self.finish_request(*args, **kws)


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
        return self.server.clients.get_total_clients()

    def get_last_message_sent(self):
        return self.server.last_message_sent


if __name__ == "__main__":
    import sys

    try:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])

        h = Houston((HOST, PORT))
        h.listen()
    except Exception as e:
        print "Error: %s" % e.message
        raise

