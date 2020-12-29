from queue import Queue
from collections import namedtuple
import threading

MoveIdfy = namedtuple('MoveIdfy',['move','depth','index'])

Total_No_Of_Tables = 40

class GameTable:
  
  def __init__(self):
    self.tables = Queue()
    for i in range(1,Total_No_Of_Tables):
      self.tables.put(i)
    self.occupied = {}
    self.vacant_evt = threading.Event()
    self.vacant_evt.set()
    self.fullhouse_evt = threading.Event()
    self.fullhouse_evt.set()

  def ReserveTable(self,move,idx=-1,depth=-1):
    self.fullhouse_evt.clear()
    vacancy = self.tables.qsize()
    if vacancy>0:
      move.gametable_id = self.tables.get()
      print(f'Reserving table {move.gametable_id}') 
      self.occupied[move.gametable_id] = MoveIdfy(move=move,depth=depth,index=idx)
      if vacancy==1:
        self.vacant_evt.clear()
    else:
      move.gametable_id = None ## better to raise a error here 
    
  def CleanTable(self,tableno):
    print(f'cleaning table {tableno}')
    del self.occupied[tableno]
    self.tables.put(tableno)
    self.vacant_evt.set()
    if self.tables.qsize()==39:
      self.fullhouse_evt.set()

  def get_vacancy(self):
    return self.tables.qsize()
  
  def MoveOf(self,gametable_no):
    if gametable_no in self.occupied:
      return self.occupied[gametable_no]
    return None
  
  def khalibiddideya(self):
    return True if self.tables.qsize()==39 else False