#!/usr/bin/python3.6

import socket
import argparse
import json
import threading
import queue
import time
import uuid

from server import dungeon_map
from server import characters
import dragon


class Server:

    instance = None

    def __init__(self, width=10, height=5):
        if Server.instance is None:
            Server.instance = Server.__DungeonServer(width, height)

    def __getattr__(self, item):
        return getattr(self.instance, item)

    class __DungeonServer:

        def __init__(self, width, height):

            self.next_new_player_number = 1
            self.sock = None
            self.threads = {}
            self.clients = {}
            self.cmds_received = queue.Queue()

            self.map = dungeon_map.Map(width, height)
            self.players = {}
            # self.connections = {}
            self.cmds = {}
            self.monsters = []

            self.action_points = 0

            self.dest_rules = {}

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

                ack = self.register_new_player(uuid)
                dragon.stream_send_dict(client, ack)

        def run(self):
            thread = threading.Thread(target=self.listen, name="Listening Thread", args=[])
            thread.start()
            while True:
                try:
                    item = self.cmds_received.get(block=False)
                    print('item:')
                    print(item)
                    if item == '':
                        continue
                    cmd_sender = item[0]
                    cmd = item[1]
                    cmd_name = cmd[0]
                    print(cmd_sender, " did something")
                    self.execute(cmd_name, cmd, cmd_sender)
                except queue.Empty:
                    time.sleep(0.01)

        def register_new_player(self, uuid, name=None, times_killed=0):
            print("registering new player")
            player_number = self.next_new_player_number
            self.next_new_player_number += 1
            if name is None:
                name = 'player' + str(player_number)
            self.players[uuid] = characters.Player(player_number, name, uuid, deaths=times_killed)
            print(type(self.players[uuid]))
            print(self.players[uuid].name, "added to the game")
            self.map.add_new_player(self.players[uuid])

            reply = dict()
            reply["event"] = "connect"
            reply["success"] = True
            reply["name"] = name
            reply["number"] = player_number
            reply["type"] = "player"
            reply["message"] = "connected successfully"
            print("DEBUG: players:")
            print(self.players)

            self.send_event({
                "message": self.players[uuid].name + " has entered the dungeon.",
                "dest": {
                    "type": "all",
                    "exclude": [uuid]
                }
            })

            self.send_event({
                "message": "welcome to the dungeon " + self.players[uuid].name,
                "dest": {
                    'type': "uuid",
                    "value": uuid
                }
            })
            return reply

        def start_socket(self):
            if self.sock is not None:
                return False

            parser = argparse.ArgumentParser(description='Video games.')
            parser.add_argument('-o', '--hostname', type=str, help='hostname to bind to (defualt: localhost)', default='0.0.0.0')
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
                print("DEBUG:")
                print(cmd_name)
                if cmd_name not in self.cmds:
                    msg = "command '"+cmd_name+"' not recognized"
                    self.send_error_event(msg, src)

                cmd = self.cmds[cmd_name]
                if hasattr(cmd, 'action_cost'):
                    action_cost = cmd.action_cost
                else:
                    action_cost = 0
                self.resolve_action_points(action_cost, src)

                events = cmd.execute(args, src)
                for event in events:
                    self.send_event(event)

            except Exception as e:
                msg = "an error occurred executing the command " + cmd_name #, "with the arguments" + str(args)
                print(e)
                print(msg)
                self.send_error_event(msg, src)

        def resolve_action_points(self, action_cost, src):
            if action_cost <= 0:
                return
            self.action_points += action_cost
            player = self.players[src]
            x, y = self.map.findPlayerByUuid(src)
            current_room = self.map.get_room(x, y)
            for entity in current_room.entities:
                if entity is player: continue
                if not hasattr(entity, "action_used"):
                    print("missing action_used:")
                    print(entity)
                    continue
                # this shouldn't be necessary, I added .action_used to all entity classes.

                events = entity.action_used(player, current_room)
                for event in events:
                    pass
                    self.send_event(event)

        def send_event(self, event):
            print('sending event:', event)
            rule_name = event["dest"]["type"]
            rule = self.dest_rules[rule_name]
            targets = rule.get_targets(event["dest"])

            if "exclude" in event["dest"]:

                to_exclude = event["dest"]["exclude"]
            else:
                to_exclude = []

            for target in targets:
                if target not in to_exclude:
                    dragon.stream_send_dict(self.clients[target], event)

        def send_error_event(self, msg, src):
            event = {
                "message": msg,
                "dest": {"type": "uuid", "value": src}
            }
            self.send_event(event)


if __name__ == "__main__":
    server = Server()
    server.start_socket()
    server.run()
