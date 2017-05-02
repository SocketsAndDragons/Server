import threading
import time


from Server.sagShell.shell import Shell
from Server.sagShell.shell import HelpCommand

PORT = 2466
HOST = '127.0.0.1'

def main():
    # TODO open welcome socket
    port = PORT
    host = HOST
    print("welcome to sockets and dragons! server is listening on port", port)
    shell = createNewShell()
    server, server_thread = start_server(host, port)
    try:
        shell.run()
    except Exception as e:
        print("an unhandled error occured")
        clean_up(server, server_thread)
        raise e

    clean_up(server, server_thread)
    print("have a nice day!")

def clean_up(server, server_thread):
    print("killing server thread")
    server.stop()
    server_thread.join(6000)


def start_server(host, port):
    server = Server(host, port)
    t = threading.Thread(target=server.start)
    t.start()
    return server, t


def createNewShell():
    shell = Shell()
    shell.gmCmd['help'] = HelpCommand()
    return shell


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.alive = True

    def start(self):
        while True:
            time.sleep(5)
            if not self.alive: break
            Shell().execute('help', ['help'])

    def stop(self):
        self.alive = False




if __name__ == "__main__":
    main()

