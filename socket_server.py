#!/usr/bin/python3.6

import socket
import argparse
import json
import dragon
import threading
import queue
import time

def accept_client(client):
	thread = threading.Thread(target=dragon.stream_parse,name="Potato",args = [client,commands])
	thread.start()

clients = {}

parser = argparse.ArgumentParser(description='Video games.')
parser.add_argument('-o', '--hostname', type=str, help = 'hostname to bind to (defualt: localhost)', default='localhost')
parser.add_argument('-p', '--port', metavar = '-p', type=int, help = 'port to listen on', default=8080)

args = parser.parse_args()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock = socket.socket()

host = args.hostname
port = args.port

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((host,port))

sock.listen(5)
commands = queue.Queue()

while True:
	client, addr = sock.accept()
	thread = threading.Thread(target=dragon.stream_parse,name="Potato",args = [client,commands])
	thread.start()
	client, addr = sock.accept()
	thread = threading.Thread(target=dragon.stream_parse,name="Spinach",args = [client,commands])
	thread.start()
	client, addr = sock.accept()
	thread = threading.Thread(target=dragon.stream_parse,name="Asbestos",args = [client,commands])
	thread.start()

	while True:
		try:
			item = commands.get(block=False)
			print(item)
		except queue.Empty:
			print("NOTHING")
			time.sleep(0.1)
