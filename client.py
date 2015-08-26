#! /usr/bin/env python

from websocket import create_connection


def main():
	ws = create_connection("ws://127.0.0.1:8080/ws", header=["Authorization: QWERTYUIOP"])
	# ws = create_connection("ws://127.0.1.1:8080/ws")
	print("Sending 'Hello, World'...")
	ws.send("Hello, World")
	print("Sent")
	print("Receiving...")
	while True:
		result =  ws.recv()
		print("Received '%s'" % result)
		# ws.close()


if __name__ == '__main__':
	main()
