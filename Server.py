import site
site.main()

from Server.sagServer import shell

PORT = 2466

def main():
    # TODO open welcome socket
    port = PORT
    print("welcome to sockets and dragons! server is listening on port", port)
    myShell = createNewShell()
    myShell.run()


def createNewShell():
    myShell = shell.Shell()
    myShell.gmCmd['help'] = shell.HelpCommand()
    return myShell


if __name__ == "__main__":
    main()

