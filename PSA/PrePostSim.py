from enum import Flag
from PickPocket.utils.StopWatch import StopWatch
import threading
from queue import Queue
import time

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

  def __init__(self,pipeline,task,gametable,Expecting_func):
    threading.Thread.__init__(self)
    self.Running = False
    self.task = task
    self.pl = pipeline
    self.gtb = gametable
    self.results = Queue()
    self.result_available_evt = threading.Event()
    self.result_available_evt.clear()
    self.isExpecting =  Expecting_func
    self.stopwatch = StopWatch() # or total execution time on unity
    self.restart_event = threading.Event()

  def run(self):
    self.Running = True
    while self.Running:
      if self.Running and self.isExpecting():
        self.pl.WaitForArrival()
        self.results.put(self.task(self.pl.recvr.RecvOne(),self.gtb))
        self.result_available_evt.set()
      else:
        print('Post Sim Thread malagtide')
        self.restart_event.clear()
        self.restart_event.wait()
  
  def GetSimResult(self):
    self.stopwatch.Start()
    self.result_available_evt.wait()
    self.stopwatch.Stop()
    if self.results.qsize()==1:
      self.result_available_evt.clear()
    return self.results.get(block=False)

  def stop(self):
    self.Running = False
    self.restart_event.set()
    self.join()
  
  def Restart(self):
    if self.Running:
      self.restart_event.set()
      print('post sim thread ebbisi aaytu')
    else:
      self.start()
      print('Post Sim Thread shuruvagide')

class MultiPreSim(threading.Thread):

  Nof_Threads = 1
  q = Queue()
  StartEvent = threading.Event()
  StopEvent = threading.Event()
  StopEvent.set()
  Running = False
  gtb = None
  
  def __init__(self,gametable):
    threading.Thread.__init__(self)

  @classmethod
  def Init(cls,nof_threads,gametable):
    cls.Nof_Threads = nof_threads
    cls.gtb = gametable
  
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
