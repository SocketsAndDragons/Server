#!/usr/bin/python3.6

import socket
import argparse
import json
import threading
import queue
import time
import uuid

from Server.server import dungeon_map
from Server.server import player
from Server import dragon


class Server:

    instance = None

    def __init__(self, width=10, height=10):
        if Server.instance is None:
            Server.instance = Server.__DungeonServer(width, height)

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __DungeonServer:

        def __init__(self, width=10, height=10):

            self.next_new_player_number = 1
            self.sock = None
            self.threads = {}
            self.clients = {}
            self.cmds_received = queue.Queue()

            self.map = dungeon_map.Map(width, height)
            self.players = {}
            self.connections = {}
            self.cmds = {}
            self.monsters = []

        def accept_new_client(self, client):
            thread = threading.Thread(target=dragon.stream_parse, name="Potato", args=[client, self.cmds_received])
            thread.start()
            return (uuid.uuid4(), thread)

        def run(self):
            while True:
                client, addr = self.sock.accept()
                print()
                uuid, thread = self.accept_new_client(client)
                print("uuid:", uuid)
                self.threads[uuid] = thread
                self.clients[uuid] = client

                ack = self.register_new_player(client)
                dragon.stream_send_dict(client, ack)

                while True:
                    try:
                        item = self.cmds_received.get(block=False)
                        print(item)
                        cmd_name = item[0]
                        self.execute(cmd_name, item, "somebody")
                    except queue.Empty:
                        time.sleep(0.1)

        def register_new_player(self, sock, name=None):
            print("registering new player")
            player_number = self.next_new_player_number
            self.next_new_player_number += 1
            if name is None:
                name = 'player' + str(player_number)
            self.players[name] = player.Player(player_number, name)
            self.connections[name] = sock

            reply = {}
            reply["event"] = "connect"
            reply["success"] = True
            reply["name"] = name
            reply["number"] = player_number
            reply["type"] = "player"
            return reply

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

        def execute(self, cmd_name, args, src):
            try:
                if cmd_name in self.cmds:
                    cmd = self.cmds[cmd_name]
                    cmd_args = cmd.execute(args, src)
                    events = cmd.get_events(cmd_args)
                    for event in events:
                        self.send_event(event)

                else:
                    print("command '"+cmd_name+"' not recognized")
            except Exception as e:
                print("an error occurred executing the command", cmd_name, "with the arguments", args)
                raise e

        def send_event(self, event):
            print('sending event:', event)
            # dragon.stream_send_dict(self.sock, event)


if __name__ == "__main__":
    server = Server()
    server.start_socket()
    server.run()





