from Server.shell import Shell


class EventPublishExceptions(Exception):
    pass


class Event:

    def __init__(self, dest, src):
        self.dest = dest
        self.src = src
        self.msg = {}

    def set_value(self, key, value):
        self.msg[key] = value;

    def publish(self):
        if self.dest.startswith("room"):
            Shell().display("send to a while room")

