from ThreadedClient import ThreadedClient as TdClient
from ThreadedServer import ThreadedServer as TdServer
import socket
from MessageQ import SQEle
import threading
import time

class PipeLine:
  def __init__(self):
    self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    self.s.bind(('',5003))
    self.s.listen(1)
    self.c,_ = self.s.accept()
    print('connected')
    self.sender = TdServer(self.c)
    self.recvr = TdClient(self.c)
  
  def open(self):
    self.sender.start()
    self.recvr.start()
  
  def close(self):
    self.sender.stop()
    self.recvr.stop()


if __name__=="__main__":
  pipeline = PipeLine()
  pipeline.open()
  count = 0
  while True:
    try:
      for msg in pipeline.recvr.RecvAll():
        count+=1
        print(msg,count)
      for i in range(10):
        pipeline.sender.Send('TESTEND_OF_MSG'.encode('ascii','replace'))
      time.sleep(1)
    except:
      pipeline.close()
      break
