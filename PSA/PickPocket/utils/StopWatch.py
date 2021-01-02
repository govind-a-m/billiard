import time

class StopWatch:

  def __init__(self):
    self.elapsed_time_s = 0
    self.start_time = None
    self.isRunning = False
  
  def Start(self):
    if not(self.isRunning):
      self.start_time = time.time()
      self.isRunning = True
  
  def Stop(self):
    if self.isRunning:
      self.elapsed_time_s = self.elapsed_time_s+time.time()-self.start_time
      self.isRunning = False

  def Reset(self):
    self.elapsed_time_s = 0
    self.isRunning = False
    self.start_time = None