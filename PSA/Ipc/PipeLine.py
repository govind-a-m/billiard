from .ThreadedClient import ThreadedClient as TdClient
from .ThreadedServer import ThreadedServer as TdServer
import socket
from .MessageQ import SQEle
import threading
import time
import json

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

  def WaitForArrival(self):
    self.recvr.Q.isnot_empty.wait()

  @property
  def NofRecvdMsgs(self):
    return self.recvr.Q.qsize()


if __name__=="__main__":
  pipeline = PipeLine()
  pipeline.open()
  fc_cmd = {'F':50,'phsi':0,'a':0,'b':0};
  pipeline.sender.Send((json.dumps(fc_cmd)+'END_OF_MSG').encode('ascii','replace'))
  while True:
    try:
      if pipeline.NofRecvdMsgs>0:
        fc_cmd['phsi'] = fc_cmd['phsi']+1.0471
        pipeline.sender.Send((json.dumps(fc_cmd)+'END_OF_MSG').encode('ascii','replace'))
        print(fc_cmd,'--------------------')
      for msg in pipeline.recvr.RecvAll():
        print(msg)
      time.sleep(0.5)
    except:
      pipeline.close()
      break

  # count = 0
  # while True:
  #   try:

  #     for msg in pipeline.recvr.RecvAll():
  #       count+=1
  #       print(msg,count)
  #     for i in range(10):
  #       pipeline.sender.Send('TESTEND_OF_MSG'.encode('ascii','replace'))
  #     time.sleep(1)
  #   except:
  #     pipeline.close()
  #     break
