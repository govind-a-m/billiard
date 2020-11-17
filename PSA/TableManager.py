from PSA.PickPocket.MoveGenerator.DirectMoveGenerator import Table,Ball

class TableManager:
  tables = {}
  count = 0

  def __init__(self):
    pass
  
  @classmethod
  def UpdateTable(cls,table_id,update_msg):
    cls.table[table_id].update_ball_loc(update_msg)

  @classmethod
  def new(cls,x,z):
    cls.cnt += 1
    table = Table(x,z,cls.cnt)
    cls.tables[cls.cnt] = table
    