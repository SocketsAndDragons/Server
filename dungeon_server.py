#!/usr/bin/python3.6

import socket
import argparse
import json
import threading
import queue
import time
import uuid

from server import dungeon_map
from server import player
import dragon


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
            id = str(uuid.uuid4())
            thread = threading.Thread(target=dragon.stream_parse, name="Potato", args=[client, self.cmds_received, id])
            thread.start()
            return (id, thread)

        def listen(self):
            while True:
                client, addr = self.sock.accept()
                print()
                uuid, thread = self.accept_new_client(client)
                print("uuid:", uuid)
                self.threads[uuid] = thread
                self.clients[uuid] = client

                ack = self.register_new_player(client)
                dragon.stream_send_dict(client, ack)

        def run(self):
            thread = threading.Thread(target=self.listen, name="Listening Thread", args=[])
            thread.start()
            while True:
                try:
                    item = self.cmds_received.get(block=False)
                    print(item)
                    # (id, action)
                    cmd_sender = item[0]
                    cmd_name = item[1][0]
                    print(cmd_sender, " did something")
                    self.execute(cmd_name, item[1][1:], cmd_sender)
                except queue.Empty:
                    time.sleep(1)
                    print("No input")

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
            reply["message"] = "connected successfully"
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
                    events = cmd.execute(args, src)
                    for event in events:
                        self.send_event(event)

                else:
                    print("command '"+cmd_name+"' not recognized")
            except Exception as e:
                print("an error occurred executing the command", cmd_name, "with the arguments", args)
                raise e

        def send_event(self, event):
            print('sending event:', event)

            targets = []

            if event["dest"]["type"] == "uuid":
                targets.append(event["dest"]["value"])
            else:
                print("I have no idea what that destination is")

            for target in targets:
                dragon.stream_send_dict(self.clients[target], event)


if __name__ == "__main__":
    server = Server()
    server.start_socket()
    server.run()
