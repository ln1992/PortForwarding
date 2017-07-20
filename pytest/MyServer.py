#coding=utf-8
#TCP服务器端程序
import socket
import time
import threading

class MyServer:
	work = 0
	res = []
	def tcplink(self,sock,addr):
		print("accept new connection from %s:%s..." % addr)
		while True:
			data=sock.recv(1024)		
			if data=='exit' or not data:
				break
			self.res.append(data)
			print "server receive " + data
			sock.send("hello: ".encode()+data)
		sock.close()
		self.work += 1
		print("Connection from %s:%s closed." % addr)

	def run(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # 创建一个基于ipv4 的TCP协议的socket
		s.bind(('127.0.0.1',11000))  #监听端口
		s.listen(5)
		print("Waiting for connection......")
		while self.work < 1:
			sock,addr=s.accept()
			t=threading.Thread(target=self.tcplink,args=(sock, addr))
			t.start()
			time.sleep(10)
		s.close()
	def getRes(self):
		return self.res

if __name__ == '__main__':
	mySe = MyServer()
	mySe.run()
	time.sleep(1)
	res = mySe.getRes()
	for i in res:
		print i
