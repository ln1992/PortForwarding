#-*- coding:utf-8 -*-

import socket
HOST = 'localhost'
PORT = 12356
ADDR =(HOST,PORT)
BUFSIZE = 1024

sock = socket.socket()
try:
    a = sock.connect(ADDR)
except Exception,e:
    print 'error',e
    sock.close()
    sys.exit()

print 'have connected with server'

while True:
    data = raw_input('> ')
    if len(data)>0:
        print 'send:',data
        sock.sendall(data) #不要用send()
        recv_data = sock.recv(BUFSIZE)
        print 'receive::',recv_data
    else:
        sock.close()
        break
