import socket
import sys
import time

class MyClient:
	def run(self,ms):
		server_address = ('localhost', 10000)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print >>sys.stderr, 'connecting to %s port %s' % server_address
		s.connect(server_address)
		for message in ms:
			# Send messages on both sockets
			print >>sys.stderr, '%s: sending "%s"' % (s.getsockname(), message)
			s.send(message)
			# Read responses on both sockets
			data = s.recv(1024)
			print >>sys.stderr, '%s: received "%s"' % (s.getsockname(), data)
			if not data:
				print >>sys.stderr, 'closing socket', s.getsockname()
				s.close()
		time.sleep(1)
		s.close()

if __name__ == '__main__':
	ms = ['111','222','333']
	myCl = MyClient()
	myCl.run(ms,)

