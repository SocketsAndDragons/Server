#!/usr/bin/python3.6

import dungeon_server
from server import dungeon_map
from server import characters

# THIS IS NOT TESTED

class UuidDestRule:

    def get_targets(self, dest_obj):
        return [dest_obj['value']]


class RoomNameDestRule:

    def get_targets(self, dest_obj):
        room_str = dest_obj['value']
        x, y = dungeon_map.getRoomAddr(room_str)
        map = dungeon_server.Server().map
        room = map.get_room(x, y)

        targets = []
        for entity in room.entities:
            if type(entity) == characters.Player:
                targets.append(entity.uuid)
        return targets


class RoomDestRule:

    def get_targets(self, dest_obj):
        x = dest_obj['x']
        y = dest_obj['y']
        map = dungeon_server.Server().map
        room = map.get_room(x, y)

        targets = []
        for entity in room.entities:
            if type(entity) == characters.Player:
                targets.append(entity.uuid)
        return targets


class GmDestRule:

    def get_targets(self, dest_obj):
        # TODO implement this
        return []


class AllDestRule:

    def get_targets(self, dest_obj):
        server = dungeon_server.Server()
        targets = []
        for uuid in server.players:
            targets.append(uuid)
        return targets


class NameDestRule:

    def get_targets(self, dest_obj):
        name = dest_obj["value"]
        server = dungeon_server.Server()
        for uuid in server.players:
            if server.players[uuid].name == name:
                return [uuid]

        return []