import threading
from queue import Queue

class PreSim(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.q = Queue()
    self.StartEvent = threading.Event()
    self.StopEvent = threading.Event()
    self.StopEvent.set()
    self.Running = False

  def run(self):
    self.Running = True
    while self.Running:
      self.StartEvent.wait()
      self.StopEvent.clear()
      presim_task = self.q.get(block=False)
      presim_task()
      if self.q.qsize()==0:
        self.StartEvent.clear()
        self.StopEvent.set()
  
  def Enq(self,task):
    self.q.put(task)
    self.StartEvent.set()
      
  def stop(self):
    self.Running = False
    self.join()

class PostSim(threading.Thread):

  def __init__(self,pipeline,task,gametable):
    threading.Thread.__init__(self)
    self.Running = False
    self.task = task
    self.pl = pipeline
    self.gtb = gametable
    self.NodeSimComplete_Event = threading.Event()

  def run(self):
    self.Running = True
    while self.Running:
      self.pl.WaitForArrival()
      self.task(self.pl.recvr.RecvOne(),self.gtb)
      if self.gtb.khalibiddideya():
        self.NodeSimComplete_Event.set()
        
  def stop(self):
    self.Running = False
    self.join()