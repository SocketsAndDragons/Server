from Server.sagServer import map
from Server.sagServer import room
from Server.sagServer import playerCommands
from Server.sagServer import gmCommands

class Shell:

    def __init__(self, width=10, height=10, startingActions=0):

        self.map = map.Map(width, height)
        self.players = []
        self.monsters = []
        self.gmCmd = {}
        self.playerCmd = {}
        self.actionPoints = startingActions


    def run(self):
        while True:
            gmIn = input("SaG?> ")
            if gmIn == 'quit' or gmIn == 'exit':
                gmIn = input('are you sure you would like to exit? (y/N)')
                if gmIn.startswith('y'):
                    break

            args = gmIn.split()
            cmdName = args[0]
            if cmdName in self.gmCmd:
                cmd = self.gmCmd[cmdName]
                cmd.execute(self, args[1:])

            else:
                print("command not recognized")



class HelpCommand:

    def __init__(self):
        self.short_help_msg = "this command prints all availible GM commands"

    def execute(self, shell, args):
        if len(args) == 0:
            self.list_all_cmds(shell)

        elif len(args) == 1:
            self.help_for_cmd(shell, args)

        else:
            print("incorrect args. try 'help' or 'helf <command name>'")

    def help(self):
        print(self.short_help_msg)

    def help_for_cmd(self, shell, args):
        cmdName = args[0]
        cmd = shell.gmCmd[cmdName]
        cmd.help()

    def list_all_cmds(self, shell):
        msg = 'the GM can use the following commands:\n'
        for cmdName in shell.gmCmd:
            msg += (cmdName+':').ljust(16)
            msg += shell.gmCmd[cmdName].short_help_msg
            msg += '\n'

        print(msg)