import threading
import time


from Server.sagServer.shell import Shell
from Server.sagServer.shell import HelpCommand

PORT = 2466
HOST = '127.0.0.1'

def main():
    # TODO open welcome socket
    port = PORT
    host = HOST
    print("welcome to sockets and dragons! server is listening on port", port)
    shell = createNewShell()
    server, server_thread = start_server(host, port, shell)
    shell.run()
    print("killing server thread")
    server.stop()
    server_thread.join(6000)
    print("have a nice day!")

def start_server(host, port, shell):
    server = Server(host, port, shell)
    t = threading.Thread(target=server.start)
    t.start()
    return server, t


def createNewShell():
    shell = Shell()
    shell.gmCmd['help'] = HelpCommand()
    return shell


class Server:

    def __init__(self, host, port, shell):
        self.host = host
        self.port = port
        self.shell = shell
        self.alive = True

    def start(self):
        while self.alive:
            time.sleep(5)
            self.shell.execute('help', ['help'])

    def stop(self):
        self.alive = False




if __name__ == "__main__":
    main()

