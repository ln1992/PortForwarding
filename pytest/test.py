from MyServer import *
from MyClient import *
from MyTrans import *
import threading

class TestClass:
	def test(self):
		mySe = MyServer()
		t1 = threading.Thread(target=mySe.run)
		t1.start()
		time.sleep(1)

		myTr = MyTrans()
		t2 = threading.Thread(target=myTr.run)
		t2.start()
		time.sleep(1)

		ms1 = ['111','222','333']
		ms2 = ['aaa','bbb','ccc']
		ms3 = ['AAA','BBB','CCC']
		myCl1 = MyClient()
		t3 = threading.Thread(target=myCl1.run, args = (ms1,))
		t3.start()
		myCl2 = MyClient()
		t4 = threading.Thread(target=myCl2.run, args = (ms2,))
		t4.start()
		myCl3 = MyClient()
		t5 = threading.Thread(target=myCl3.run, args = (ms3,))
		t5.start()

		time.sleep(8)
		res = mySe.getRes()
		ms = ms1 + ms2 + ms3

		res.sort()
		ms.sort()
		assert len(res) == len(ms)
		for i in range(0, len(res)):
			print res[i] + ms[i]
			assert res[i] == ms[i]

#if __name__ == '__main__':
