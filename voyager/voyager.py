import socket
import thread


class Voyager:

    def __init__(self, config):
        self.config = config
        self.sock = None
        self.last_message_sent = ''
        self.thread_read = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.config)
        self.thread_read = thread.start_new_thread(self.read_anserws, ())

    def read_anserws(self):
        while True:
            msg = self.sock.recv(1024)
            if not msg:
                break
            self.last_message_sent += msg
            print("Voyager Recebeu: {}".format(msg))

    def get_last_message_sent(self):
        return self.last_message_sent

    def close(self):
        self.sock.close()
