import threading
from .MessageQ import SendQ

class ThreadedServer(threading.Thread):
	def __init__(self,s):
		threading.Thread.__init__(self)
		self.s = s
		self.Running = False
		self.Q = SendQ()

	def run(self):
		self.Running = True
		while self.Running:
			self.Q.isnot_empty.wait()
			msg = self.Q.get()
			self.s.sendall(msg)
		

	def Send(self,msg):
		self.Q.put(msg)

	def stop(self):
		self.Running = False
		self.join()


if __name__ == "__main__":
	ThreadSock = ThreadedServer(lambda : b"TEST" ,lambda x: print(x))
	ThreadSock.start()
