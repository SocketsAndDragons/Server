import json

def moved(success):
	event = {}
	event["name"] = "moved"
	event["success"] = success
	return event

def look(room,entities,items,peeking):
	event = {}
	event["name"] = "look"
	event["room"] = room
	event["entities"] = entities
	event["items"] = items
	event["peeking"] = peeking
	return event

def hear(text, speaker):
	event = {}
	event["name"] = "hear"
	event["text"] = text
	event["speaker"] = speaker
