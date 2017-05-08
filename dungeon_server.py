#!/usr/bin/python3.6

import socket
import argparse
import json
import threading
import queue
import time
import uuid

from Server.server import dungeonMap
from Server import dragon


class DungeonServer:

    instance = None

    def __init__(self, width=10, height=10):
        if DungeonServer.instance is None:
            DungeonServer.instance = DungeonServer.__DungeonServer(width, height)

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __DungeonServer:

        def __init__(self, width=10, height=10):

            self.sock = None
            self.threads = {}
            self.clients = {}
            self.cmds_received = queue.Queue()

            self.map = dungeonMap.Map(width, height)
            self.players = []
            self.monsters = []
            self.cmds = {}

        def accept_new_client(self, client):
            thread = threading.Thread(target=dragon.stream_parse, name="Potato", args=[client, self.cmds_received])
            thread.start()
            return (uuid.uuid4(), thread)

        def run(self):
            while True:
                client, addr = self.sock.accept()
                print()
                uuid, thread = self.accept_new_client(client)
                self.threads[uuid] = thread
                self.clients[uuid] = client

                while True:
                    try:
                        item = self.cmds_received.get(block=False)
                        print(item)
                    except queue.Empty:
                        time.sleep(0.1)

        def start_socket(self):
            if self.sock is not None:
                return False

            parser = argparse.ArgumentParser(description='Video games.')
            parser.add_argument('-o', '--hostname', type=str, help='hostname to bind to (defualt: localhost)', default='localhost')
            parser.add_argument('-p', '--port', metavar='-p', type=int, help='port to listen on', default=8080)

            args = parser.parse_args()

            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.sock = socket.socket()

            host = args.hostname
            port = args.port

            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind((host, port))
            self.sock.listen(5)

            print("created socket")
            print("host:", host)
            print("port:", port)


if __name__ == "__main__":
    server = DungeonServer()
    server.start_socket()
    server.run()





