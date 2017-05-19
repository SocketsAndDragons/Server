import socket
import argparse
import json
import time
import logging
import sys

# uncomment to see detailed info
#logging.basicConfig(level=logging.INFO)


def peel_size(data,pos):
	size = int.from_bytes(data[pos:pos+4],byteorder='big')
	return (size,pos+4)

def peel_json(data,pos,size_left):
	packet_size = len(data)
	if len(data) - pos < size_left:
		return (data[pos:], packet_size, size_left - (packet_size-pos))
	else:
		end = pos + size_left
		return (data[pos:end], end, 0)

def debug_log(msg,debug):
	if debug:
		log(msg)

def stream_parse(socket,queue,tag=None,format='dict'):

	# Size of the next JSON unit
	size = None
	# Size of the data unit we're parsing
	packet_size = 0
	# Position in the data unit
	pos = 0
	# How much more data we expect from the next JSON unit
	size_left = 1
	# The actual message being decoded
	msg = ""
	# The data unit
	data = None
	# The end of the previous message unit, if we need to keep it (too small to read the next packet size!)
	prev_data = b''

	# Don't thrash my CPU so hard
	time.sleep(0.001)
	try:
		while True:
			# A packet is done.
			if size_left <= 0:
				logging.info("Packet done: " + msg)
				if format == 'json':
					queue.put((tag,msg))
				elif format == 'dict':
					queue.put((tag,json.loads(msg)))
				size = None
				msg = ""
				size_left = 1

			# We're out of data.
			if pos >= packet_size:
				data = prev_data + socket.recv(1024)
				pos = 0
				packet_size = len(data)


			while pos < packet_size and size_left > 0:
				# Start reading a new packet.
				if not size:
					# We have enough data to peel off the size
					if pos + 4 <= packet_size:
						(size,pos) = peel_size(data,pos)
						size_left = size
					# Not enough bytes. Keep these bytes, and request more data
					else:
						prev_data = data[pos:packet_size]
						pos = packet_size
				# We're reading a packet
				else:
					(new_json, pos, size_left) = peel_json(data, pos, size_left)
					msg += new_json.decode("utf-8")
					logging.info("Status: %d, %d, %d",pos,size,size_left)
	except ConnectionResetError as e:
		queue.put([tag, ["disconnect"]])
		sys.exit(-2)

def stream_send_dict(socket,dict):
	stream_send(socket, json.dumps(dict))

def stream_send(socket,json):
	data = json.encode("utf-8")
	data = len(data).to_bytes(4, byteorder='big') + data
	logging.info("Sending packet: ")
	logging.info(repr(data))
	socket.send(data)
