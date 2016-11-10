import unittest
import socket
import time
import random

from voyager.houston import Houston
from voyager.voyager import Voyager
from voyager.mission_control import MissionControl


class SocketServerTestCase(unittest.TestCase):

    def test_open_connection(self):

        config = ('0.0.0.0', 1234)
        server = Houston(config)
        server.listen()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertEqual(result, 0)

    def test_close_connection(self):
        config = ('0.0.0.0', 1235)
        server = Houston(config)
        server.listen()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertEqual(result, 0)

        server.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(config)
        self.assertNotEqual(result, 0)

    def test_accept_one_client_connections(self):

        config = ('0.0.0.0', 1236)
        server = Houston(config)
        server.listen()

        client1 = Voyager(config)
        client1.connect()

        time.sleep(1)

        self.assertEqual(server.count_clients(), 1)

    def test_accept_any_client_connections(self):
        config = ('0.0.0.0', 1237)
        server = Houston(config)
        server.listen()

        client1 = Voyager(config)
        client1.connect()

        time.sleep(1)

        client2 = Voyager(config)
        client2.connect()

        time.sleep(1)

        client3 = Voyager(config)
        client3.connect()

        time.sleep(1)

        self.assertEqual(server.count_clients(), 3)

    def test_mission_control_connection_on_server(self):
        config = ('0.0.0.0', 1238)
        server = Houston(config)
        server.listen()

        try:
            mission = MissionControl(config)
            mission.connect()
            self.assertTrue(True)
        except Exception as e:
            self.assertFalse(True)

        server.close()

    def test_mission_control_sending_message_to_server(self):
        config = ('0.0.0.0', 1239)
        server = Houston(config)
        server.listen()

        client1 = Voyager(config)
        client1.connect()

        mission = MissionControl(config)
        mission.connect()
        mission.send('hello')

        time.sleep(1)

        self.assertEqual(server.get_last_message_sent(), 'hello')

    def test_mission_control_sending_message_to_clientes(self):

        config = ('0.0.0.0', random.randrange(1000, 1999))
        server = Houston(config)
        server.listen()

        client1 = Voyager(config)
        client1.connect()

        time.sleep(2)

        mission = MissionControl(config)
        mission.connect()
        mission.send('hello')

        time.sleep(2)

        server.close()
        # client1.close()
        # mission.close()

        self.assertEqual(server.count_clients(), 2)
        self.assertEqual(client1.get_last_message_sent(), 'hello')
