import json

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
