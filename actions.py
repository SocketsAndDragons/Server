import json

class InvalidCommandException(Exception):
	pass

class InvalidArgumentException(Exception):
	pass

def parse(input):
	cmd = input.split(" ")[0]
	if cmd == "look":
		return look()
	if cmd == "say":
		return say(input.split(" ", 1)[1])
	if cmd == "whisper":
		return whisper(input.split(" ")[1], input.split(" ",2)[2])
	else:
		raise Exception

# Meta

def join(player):
	action = {}
	action["name"] = "join"
	action["player"] = player
	return action

def quit():
	action = {}
	action["name"] = "quit"
	return action

# Gameplay
def look():
	action = {}
	action["name"] = "look"
	return action

def say(text):
	action = {}
	action["name"] = "say"
	action["text"] = text
	return action

def whisper(target, text):
	action = {}
	action["name"] = "whisper"
	action["text"] = text
	action["target"] = target
	return action

def quit():
	action = {}
