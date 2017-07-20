# echo server example
import select
import socket
import sys
import Queue
import time

class MyTrans:
	def run(self):
		server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		server.setblocking(0)
		server_address = ('localhost', 10000)
		print >>sys.stderr, 'starting up on %s port %s' % server_address
		server.bind(server_address)
		server.listen(5)
		inputs = [ server ]
		outputs = [ ]
		message_queues = {}

		outServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outServer.connect(('localhost', 11000))

		work = 0
		#while inputs:
		while work < 3:
			# Wait for at least one of the sockets to be ready for processing
			print >>sys.stderr, 'waiting for the next event'
			readable, writable, exceptional = select.select(inputs, outputs, inputs)
		   
			# Handle inputs
			for s in readable:
				if s is server:
				    # A "readable" socket is ready to accept a connection
					connection, client_address = s.accept()
					print >>sys.stderr, ' connection from', client_address
					connection.setblocking(0)
					inputs.append(connection)
				   
				    # Give the connection a queue for data we want to send
					message_queues[connection] = Queue.Queue()
				else:
					data = s.recv(1024)
					if data:
				        # A readable client socket has data
						print >>sys.stderr, ' received "%s" from %s' % (data, s.getpeername())
						message_queues[s].put(data)
				        # Add output channel for response
						if s not in outputs:
							outputs.append(s)
					else:
				        # Interpret empty result as closed connection
						print >>sys.stderr, ' closing', client_address
				        # Stop listening for input on the connection
						if s in outputs:
							outputs.remove(s)
				       
						inputs.remove(s)
						s.close()
						work += 1
				       
				        # Remove message queue
						del message_queues[s]

			# Handle outputs
			for s in writable:
				try:
					next_msg = message_queues[s].get_nowait()
					outServer.send(next_msg)
					data = outServer.recv(1024)
					if not data:
						print >>sys.stderr, 'closing out server socket', s.getsockname()
						outServer.close()
				except Queue.Empty:
				    # No messages waiting so stop checking for writability.
				    print >>sys.stderr, ' ', s.getpeername(), 'queue empty'
				    outputs.remove(s)
				else:
				    print >>sys.stderr, ' sending "%s" to %s' % (next_msg, s.getpeername())
				    s.send(next_msg)
				       
			# Handle "exceptional conditions"
			for s in exceptional:
				print >>sys.stderr, 'exception condition on', s.getpeername()
				# Stop listening for input on the connection
				inputs.remove(s)
				if s in outputs:
				    outputs.remove(s)
				s.close()
			   
				# Remove message queue
				del message_queues[s]
			#time.sleep(1)

		time.sleep(5)
		outServer.close()
		server.close()

if __name__ == '__main__':
	myTr = MyTrans()
	myTr.run()

