import unittest

import socket
from time import sleep
from voyager.voyager1 import Voyager1
from voyager.voyager2 import Voyager2
from voyager.houston import Houston
import subprocess

HOST = '0.0.0.0'


class HoustonTestCase(unittest.TestCase):

    houston = None

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_bind_port(self):
        port = 1212
        houston = Houston(HOST, port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, port))
        self.assertEqual(result, 0)

        houston.close()

    def test_close_port(self):
        port = 1213

        houston = Houston(HOST, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, port))
        self.assertEqual(result, 0)
        houston.close()

        sleep(1)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((HOST, port))
        self.assertNotEqual(result, 0)

    def test_send_commands_to_all_client_with_one_client(self):
        port = 1214
        whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE).stdout.read()

        houston = Houston(HOST, port)
        sleep(2)
        client_one = Voyager1(HOST, port)
        sleep(2)

        houston.sendCommandAllPeer('whoami')
        sleep(2)
        self.assertEqual(client_one.last_run.command.output, whoami)
        client_one.close()
        houston.close()

    def test_send_commands_to_all_client_with_any_client(self):
        port = 1215
        whoami = subprocess.Popen("whoami", shell=True, stdout=subprocess.PIPE).stdout.read()

        houston = Houston(HOST, port)
        sleep(2)

        client_one = Voyager1(HOST, port)
        client_two = Voyager1(HOST, port)
        client_three = Voyager1(HOST, port)
        sleep(2)

        houston.sendCommandAllPeer('whoami')
        sleep(2)

        self.assertEqual(client_one.last_run.command.output, whoami)
        self.assertEqual(client_two.last_run.command.output, whoami)
        self.assertEqual(client_three.last_run.command.output, whoami)
        client_one.close()
        client_two.close()
        client_three.close()
        houston.close()

    def test_run_commands_to_all_clients_by_voyager2(self):
        port = 1216
        command = 'whoami'
        whoami = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
        houston = Houston(HOST, port)
        sleep(2)

        client_one = Voyager1(HOST, port)
        client_two = Voyager1(HOST, port)
        sleep(2)

        voyager2 = Voyager2(HOST, port)
        sleep(2)
        voyager2.sendCommandsAllPeers(command)
        sleep(2)

        self.assertEqual(client_one.last_run.command.output, whoami)
        self.assertEqual(client_two.last_run.command.output, whoami)

        client_one.close()
        client_two.close()

        houston.close()
        voyager2.close()


if __name__ == '__main__':
    unittest.main()
