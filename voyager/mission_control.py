import socket


class MissionControl:

    def __init__(self, config):
        self.config = config
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.config)

    def send(self, message):
        print("Mission sad: {}".format(message))
        self.sock.sendall("Mission sad: {}".format(message))

    def close(self):
        self.sock.close()