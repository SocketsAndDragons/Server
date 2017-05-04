#!/usr/bin/python3

import dragon
import socket
import threading
import queue
import time
import actions
import events
import json

def game_loop(sock,inputs,resps):
	while True:
		# Handle server messages
		try:
			item = resps.get(block=False)
			print(item)
		except queue.Empty:
			time.sleep(0.1)
		# Handle inputs
		try:
			item = inputs.get(block=False)
			print("Sending ",item)
			dragon.stream_send_dict(sock,item)
		except queue.Empty:
			time.sleep(0.1)


s = socket.socket()

s.connect(('localhost',8080))

print("YAYAYY")

inputs = queue.Queue()
resps = queue.Queue()

thread = threading.Thread(target=dragon.stream_parse,name="Listener",args = [s,resps])
thread.start()
thread = threading.Thread(target=game_loop,name="Input",args = [s,inputs,resps])
thread.start()
while True:
	cmd = input("Gimme something to do ===>>  ")
	act = actions.parse(cmd)
	inputs.put(act)
