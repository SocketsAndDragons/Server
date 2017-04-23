import threading
import time


from Server.sagServer.shell import Shell
from Server.sagServer.shell import HelpCommand

PORT = 2466

def main():
    # TODO open welcome socket
    port = PORT
    print("welcome to sockets and dragons! server is listening on port", port)
    shell = createNewShell()
    server_thread = start_server(shell)
    shell.run()
    print("killing server thread")
    server_thread.isAlive = False
    server_thread.join(5000)
    print("have a nice day!")

def start_server(shell):
    t = threading.Thread(target=run_server, args=(shell,))
    t.start()
    return t

def run_server(shell):
    while True:
        time.sleep(5)
        shell.execute('help', ['help'])

def createNewShell():
    shell = Shell()
    shell.gmCmd['help'] = HelpCommand()
    return shell


if __name__ == "__main__":
    main()

