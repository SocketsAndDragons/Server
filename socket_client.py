#!/usr/bin/python3

import dragon
import socket
import threading
import queue
import time

def game_loop(sock,inputs,resps):
	while True:
		# Handle server messages
		try:
			item = resps.get(block=False)
			print(item)
		except queue.Empty:
			print("Nothing from the server")
			time.sleep(1)
		# Handle inputs
		try:
			item = inputs.get(block=False)
			print("Sending ",item)
			dragon.stream_send(sock,item)
		except queue.Empty:
			print("No command to send!")
			time.sleep(1)


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
	inputs.put(cmd)
