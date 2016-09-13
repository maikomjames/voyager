import unittest

import socket
import thread
from time import sleep
from voyager.voyager1 import Voyager1
from voyager.houston import Houston
from voyager.config import HOST, PORT


class HoustonTestCase(unittest.TestCase):

    houston = None

    def setUp(self):
        self.houston = Houston(HOST, PORT)
        sleep(2)

    def tearDown(self):
        self.houston.close()
        sleep(2)

    def test_bind_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, PORT))
        self.assertEqual(result, 0)

    def test_send_commands_to_all_client_with_one_client(self):
        client_one = Voyager1(HOST, PORT)
        sleep(2)
        self.houston.sendCommandAllPeer('whoami')
        sleep(2)
        self.assertEqual(client_one.last_run.command.output, 'maikom\n')
        client_one.close()


    def test_send_commands_to_all_client_with_any_client(self):
        client_one = Voyager1(HOST, PORT)
        client_two = Voyager1(HOST, PORT)
        client_three = Voyager1(HOST, PORT)
        sleep(2)
        self.houston.sendCommandAllPeer('whoami')
        sleep(2)
        self.assertEqual(client_one.last_run.command.output, 'maikom\n')
        self.assertEqual(client_two.last_run.command.output, 'maikom\n')
        self.assertEqual(client_three.last_run.command.output, 'maikom\n')
        client_one.close()
        client_two.close()
        client_three.close()


if __name__ == '__main__':
    unittest.main()
