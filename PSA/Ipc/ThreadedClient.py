import threading
from MessageQ import RecvQ,SQEle

class ThreadedClient(threading.Thread):
  def __init__(self,s):
    threading.Thread.__init__(self)
    self.s = s
    self.Running = False
    self.Q = RecvQ()
    self.isnot_empty = threading.Event()

  def run(self):
    self.Running = True
    recv_data = ''
    while self.Running:
      recv_data = recv_data+self.s.recv(1024).decode()
      while (EOM_idx := recv_data.find('END_OF_MSG'))>0:
        self.Q.put(recv_data[:EOM_idx])
        recv_data = recv_data[EOM_idx+10:]
  
  def RecvOne(self):
    return self.Q.get()

  def RecvAll(self):
      while ret:=self.RecvOne():
      yield ret

  def stop(self):
    self.Running = False
    self.join()
