import socket
import thread


class Houston:

    def __init__(self, *args, **kw):
        self.config = args[0]
        self.sock = None
        self.thread = None
        self.message = ''
        self.clients = HoustonClientList()
        self.request_listener = None

    def bind(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(self.config)

    def listen(self):
        self.bind()
        self.sock.listen(1)

        self.request_listener = HoustonRequestListener(self)
        self.thread = thread.start_new_thread(self.request_listener.listener, ())

    def close(self):
        self.sock.close()

    def get_last_message(self):
        return self.message


class HoustonClientList:

    def __init__(self, *args, **kwargs):
        self.clients = []

    def add(self, client):
        self.clients.append(client)

    def count(self):
        return len(self.clients)


class HoustonClient:
    def __init__(self, *args, **kwargs):
        self.id = kwargs.get('id')
        self.client_address = kwargs.get('client_address')
        self.connection = kwargs.get('connection')


class HoustonRequestListener:

    def __init__(self, *args, **kw):
        self.server = args[0]
        self.sock = self.server.sock
        self.thread = None

    def listener(self):
        while True:
            try:
                connection, client_address = self.sock.accept()

                self.server.clients.add(
                    HoustonClient(id='abdce', client_address=client_address, connection=connection)
                )
                listener_message = HoustonThreadListenerMessages(self.server, connection, client_address)
                self.thread = thread.start_new_thread(listener_message.listener, ())
            except Exception as e:
                # print("Error - : {}".format(e.message))
                pass


class HoustonThreadListenerMessages:

    def __init__(self, *args, **kw):
        self.server = args[0]
        self.connection = args[1]
        self.client_address = args[2]
        self.message = ''

    def listener(self):
        while True:
            data = self.connection.recv(1024)
            print('Message: {}'.format(data))
            if not data:
                break
            self.message += data
            self.server.message = self.message


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
