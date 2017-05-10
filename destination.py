#!/usr/bin/python3.6

import dungeon_server

# THIS IS NOT TESTED

class UuidDestRule:

    def get_targets(self, dest_obj):
        return [dest_obj['value']]


class RoomDestRule:

    def get_targets(self, dest_obj):
        map = dungeon_server.Server().map
        # TODO implement this
        return []


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
        # TODO implement this
        return targets


class NameDestRule:

    def get_targets(self, dest_obj):
        name = dest_obj["value"]
        server = dungeon_server.Server()
        for uuid in server.players:
            if server.players[uuid].name == name:
                return [uuid]

        return []