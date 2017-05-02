
import sys
from Server.server import map
from Server.server import room
from Server.server import playerCmds
from Server.server import gmCmds

INSTANCE = None

class Shell:
    class __Shell:
        CMD_PROMPT = 'SaG?> '
        DEBUG = True

        def __init__(self, width=10, height=10, startingActions=0):

            self.map = map.Map(width, height)
            self.players = []
            self.monsters = []
            self.gmCmd = {}
            self.playerCmd = {}
            self.actionPoints = startingActions

        def run(self):
            self.display()
            while True:
                gmIn = input()
                if gmIn == 'quit' or gmIn == 'exit':
                    gmIn = input('are you sure you would like to exit? (y/N)')
                    if gmIn.startswith('y'):
                        break

                args = gmIn.split()
                self.execute(args[0], args)

        def execute(self, cmdName, args):
            try:
                if cmdName in self.gmCmd:
                    cmd = self.gmCmd[cmdName]
                    success = cmd.execute(args)
                else:
                    self.display("command not recognized")
            except Exception as e:
                self.display("an error occurred executing the command", cmdName,"with the arguments", args)
                raise e

        def display(self, *args, lastMsg=True, debug=False):
            # do not print debug messages outside debugt mode
            if (debug and not self.DEBUG): return

            msg = ''
            for arg in args:
                msg += str(arg)
                msg += ' '
            print(msg)
            if lastMsg:
                sys.stdout.write(self.CMD_PROMPT)
                sys.stdout.flush()
    instance = None

    def __init__(self, width=10, height=10, startingActions=0):
        if Shell.instance is None:
            Shell.instance = Shell.__Shell(width, height, startingActions)

    def __getattr__(self, item):
        return getattr(self.instance, item)

class HelpCommand:

    def __init__(self):
        self.short_help_msg = "this command prints all availible GM commands"

    def execute(self, args):
        if len(args) == 1:
            self.list_all_cmds()

        elif len(args) == 2:
            self.help_for_cmd(args)

        else:
            Shell().display("incorrect args. try 'help' or 'helf <command name>'")
            return False
        return True

    def help(self):
        Shell().display(self.short_help_msg)

    def help_for_cmd(self, args):
        cmdName = args[0]
        cmd = Shell().gmCmd[cmdName]
        cmd.help()

    def list_all_cmds(self):
        msg = 'the GM can use the following commands:\n'
        for cmdName in Shell().gmCmd:
            msg += (cmdName+':').ljust(16)
            msg += Shell().gmCmd[cmdName].short_help_msg
            msg += '\n'

        Shell().display(msg)