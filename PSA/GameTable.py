from collections import namedtuple

Total_No_Of_Tables = 40
Name_Suffix = "GameTable_"

TableMap = namedtuple('gametable','table_id')

class GameTable:
  tables = {}
  GameTable_Table = {}
  ActiveList = []

  def __init__(self,name):
    self.name = name
    self.active = False
    self.AssignedTable = None

  @classmethod
  def Init(cls):
    for i in range(2,Total_No_Of_Tables+1):
      cls.tables[Name_Suffix+str(i)] = TableMap(cls(Name_Suffix+str(i)),None)
      cls.ActiveList.append(Name_Suffix+str(i))
  
  @classmethod
  def ReserveTable(cls,table):
    if len(cls.ActiveList)>0:
      gametable = cls.GameTable_Table[cls.ActiveList[0]].gametable
      gametable.table_id = table_id
      gametable.active = True
      gametable.AssignedTable = table
      return gametable
    return None
  
  def Simulate(move):



