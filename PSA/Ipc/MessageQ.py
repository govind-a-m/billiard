from queue import Queue
import threading

class SQEle:
  def __init__(self,data,callback):
    self.data = data
    self.callback = callback

  def ServiceCallback(self):
    self.callback()

class Qbase(Queue):
  def __init__(self):
    Queue.__init__(self)
    self.isnot_empty = threading.Event()

  def get(self):
    if self.qsize()>0:
      ret = Queue.get(self,block=False)
    else:
      return None
    if self.qsize()==0:
      self.isnot_empty.clear()
    return ret

  def put(self,msg):
    Queue.put(self,msg)
    self.isnot_empty.set()

class SendQ(Qbase):
  def __init__(self):
    Qbase.__init__(self)


class RecvQ(Qbase):
  def __init__(self):
    Qbase.__init__(self)
  
  