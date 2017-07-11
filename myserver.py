#-*- coding:utf-8 -*-
from SocketServer import BaseRequestHandler,ThreadingTCPServer,ForkingTCPServer
import threading

BUF_SIZE=1024

class Handler(BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(BUF_SIZE)
            if len(data)>0:
                print 'receive=',data
                cur_thread = threading.current_thread()
                response = '{}:{}'.format(cur_thread.ident,data)
                self.request.sendall(response)
                print 'send:',response
            else:
                print 'close'
                break



if __name__ == '__main__':
    HOST = ''
    PORT = 12356
    ADDR = (HOST,PORT)
   # server = ForkingTCPServer(ADDR,Handler)  #参数为监听地址和已建立连接的处理类
    server = ThreadingTCPServer(ADDR,Handler)
    print 'listening'
    server.serve_forever()  #监听，建立好TCP连接后，为该连接创建新的socket和线程，并由处理类中的handle方法处理
