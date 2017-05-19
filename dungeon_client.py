#!/usr/bin/python3

import sys
import dragon
import socket
import threading
import queue
import time
import json
import readline

THREADS = []
USERNAME = None
SHARED = {"username": None}


def prompt():
	username = SHARED["username"]
	if username is None:
		return ''
	return "dungeon-client " + username + " >>> "


def game_loop(sock,inputs,resps):
	print_prompt = False
	username = None
	while True:
		# Handle server messages
		try:
			item = resps.get(block=False)
			print()
			if "event" in item[1]:
				# print("DEBUG:")
				# print(item[1])
				if item[1]["event"] == "connect" and "name" in item[1]:
					SHARED["username"] = item[1]["name"]
			if "message" in item[1]:
				sys.stdout.write(item[1]["message"])
				sys.stdout.write("\n")
				# sys.stdout.write(prompt())
				# sys.stdout.flush()
				print_prompt = True

		except queue.Empty:
			time.sleep(0.1)
			if print_prompt:
				sys.stdout.write(prompt())
				sys.stdout.flush()
				print_prompt = False

		# Handle inputs
		try:
			item = inputs.get(block=False)
			dragon.stream_send_dict(sock,item)
		except queue.Empty:
			time.sleep(0.01)

hostport = input("Enter the hostname and port of the server (hostname:port) ===>>  ").split(":")

try:
	host = hostport[0]
	port = hostport[1]
except:
	print("invalid path entered!")
	sys.exit(-1)

try:
	print("\n\n\n")
	s = socket.socket()

	s.connect((host,int(port)))

	print("Connection made. Logging in...")

	inputs = queue.Queue()
	resps = queue.Queue()

	thread = threading.Thread(target=dragon.stream_parse,name="Listener",args = [s,resps])
	thread.start()
	THREADS.append(thread)

	thread = threading.Thread(target=game_loop,name="Input",args = [s,inputs,resps])
	thread.start()
	THREADS.append(thread)
except:
	print("Failed to connect! You died")

try:
	while True:
		cmd = input(prompt())
		act = cmd.split()
		inputs.put(act)

		if cmd.startswith('disconnect '):
			print("disconnecting!")
			sys.exit(0)
except:
	print("connection lost!! :(")
finally:
	sys.exit(1)
