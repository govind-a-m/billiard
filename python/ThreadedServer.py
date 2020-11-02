import time
import zmq
import threading

class ThreadedServer(threading.Thread):
	def __init__(self,send_func,recv_func):
		threading.Thread.__init__(self)
		self.context = zmq.Context()
		self.socket = self.context.socket(zmq.REP)
		self.socket.bind("tcp://*:5555")
		self.send_func = send_func
		self.recv_func = recv_func
		self.RESP_REQ_State = "REQ"
		self.Running = False

	def run(self):
		Running = True
		while Running:
			if self.RESP_REQ_State=="REQ":
				self.recv_func(self.socket.recv())
				self.RESP_REQ_State = "RESP"
			else:
				self.socket.send(self.send_func())
				self.RESP_REQ_State = "REQ"

	def stop(self):
		self.Running = False
		self.join()


if __name__ == "__main__":
	ThreadSock = ThreadedServer(lambda : b"TEST" ,lambda x: print(x))
	ThreadSock.start()
