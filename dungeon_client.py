#!/usr/bin/python3

import sys
import dragon
import socket
import threading
import queue
import time
import json

THREADS = []

def game_loop(sock,inputs,resps):
	while True:
		# Handle server messages
		try:
			item = resps.get(block=False)
			print("Received: ")
			print(item[1]["message"])
		except queue.Empty:
			time.sleep(0.01)
		# Handle inputs
		try:
			item = inputs.get(block=False)
			dragon.stream_send_dict(sock,item)
		except queue.Empty:
			time.sleep(0.01)

print("Welcome to die")

hostport = input("Enter the hostname and port of the server (hostname:port) ===>>  ").split(":")

host = hostport[0]
port = hostport[1]

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

	while True:
		cmd = input("Gimme something to do ===>>  ")
		if cmd.startswith('..'):
			sys.exit(0)

		act = cmd.split()
		inputs.put(act)
except:
	print("Failed to connect! You died")
finally:
	sys.exit(1)
