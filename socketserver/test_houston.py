import unittest
import random
import socket
import time

from socketserver.houston import Houston


class HoustonTestCase(unittest.TestCase):

    def tearDown(self):
        time.sleep(1)

    def test_open_socket_connection_server(self):
        config = ('0.0.0.0', 1234)
        server = Houston(config)
        server.listen()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertEqual(result, 0)

    def test_close_socket_connection_server(self):
        config = ('0.0.0.0', 1444)
        server = Houston(config)
        server.listen()

        time.sleep(0.5)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertEqual(result, 0)

        server.close()

        time.sleep(0.5)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertNotEqual(result, 0)

    def test_read_message_sent(self):
        config = ('0.0.0.0', 1236)
        print(config)
        server = Houston(config)
        server.listen()

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(config)
        client.send('hello')

        time.sleep(0.5)

        self.assertEqual(server.get_last_message(), 'hello')

    def test_read_message_sent_with_two_clients(self):
        config = ('0.0.0.0', 1237)
        print(config)
        server = Houston(config)
        server.listen()

        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect(config)
        client1.send("I'm client 1")
        time.sleep(0.5)
        self.assertEqual(server.get_last_message(), "I'm client 1")

        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect(config)
        client2.send("I'm client 2")
        time.sleep(0.5)
        self.assertEqual(server.get_last_message(), "I'm client 2")

        client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client3.connect(config)
        client3.send("I'm client 3")
        time.sleep(0.5)
        self.assertEqual(server.get_last_message(), "I'm client 3")

    def test_count_clients_connected(self):
        config = ('0.0.0.0', 1238)
        print(config)
        server = Houston(config)
        server.listen()

        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect(config)
        client1.send("I'm client 1")

        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect(config)
        client2.send("I'm client 2")

        client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client3.connect(config)
        client3.send("I'm client 3")

        self.assertEqual(server.clients.count(), 3)

    def test_count_clients_connected_and_sending_two_messagens(self):
        config = ('0.0.0.0', 1239)
        print(config)
        server = Houston(config)
        server.listen()

        client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client1.connect(config)
        client1.send("I'm client 1")
        client1.send("I'm client 1 again")

        client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client2.connect(config)
        client2.send("I'm client 2")
        client2.send("I'm client 2 again")

        client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client3.connect(config)
        client3.send("I'm client 3")
        client3.send("I'm client 3 again")

        time.sleep(0.5)

        self.assertEqual(server.clients.count(), 3)


if __name__ == '__main__':
    unittest.main()
