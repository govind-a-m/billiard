import threading
from queue import Queue

class PreSim(threading.Thread):

  def __init__(self,gametable):
    threading.Thread.__init__(self)
    self.q = Queue()
    self.StartEvent = threading.Event()
    self.StopEvent = threading.Event()
    self.StopEvent.set()
    self.Running = False
    self.gtb = gametable

  def run(self):
    self.Running = True
    while self.Running:
      self.StartEvent.wait()
      self.StopEvent.clear()
      self.gtb.vacant_evt.wait()
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
    self.results = Queue()
    self.result_available_evt = threading.Event()
    self.result_available_evt.clear()

  def run(self):
    self.Running = True
    while self.Running:
      self.pl.WaitForArrival()
      self.results.put(self.task(self.pl.recvr.RecvOne(),self.gtb))
      self.result_available_evt.set()
  
  def GetSimResult(self):
    self.result_available_evt.wait()
    if self.results.qsize()==1:
      self.result_available_evt.clear()
    return self.results.get(block=False)

  def stop(self):
    self.Running = False
    self.join()