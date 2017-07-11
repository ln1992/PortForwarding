#-*- coding:utf-8 -*-
from SocketServer import BaseRequestHandler,ThreadingTCPServer
import threading
import socket

BUF_SIZE=1024

class Handler(BaseRequestHandler):
    def handle(self):
        sock = socket.socket()
        try:
            a = sock.connect(('localhost', 12356))
        except Exception,e:
            print 'error',e
            sock.close()
            sys.exit()
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                print 'receive=',data
                cur_thread = threading.current_thread()
                response = '{}:{}'.format(cur_thread.ident,data)
                self.request.sendall(response)
                print 'send:',response
                sock.sendall(data) #不要用send()
                recv_data = sock.recv(BUF_SIZE)
                print 'receive::',recv_data
            else:
				sock.close()
				print 'close'
				break


if __name__ == '__main__':
    HOST = ''
    PORT = 7000
    ADDR = (HOST,PORT)  
    server = ThreadingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
    print 'listening'
    server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理 
