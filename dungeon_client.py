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
			time.sleep(0.1)
		# Handle inputs
		try:
			item = inputs.get(block=False)
			print("Sending ",item)
			dragon.stream_send_dict(sock,item)
		except queue.Empty:
			time.sleep(0.1)

try:
	s = socket.socket()

	s.connect(('localhost',8080))

	print("YAYAYY")

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

finally:
	sys.exit(1)
