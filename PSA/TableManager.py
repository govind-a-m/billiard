from PickPocket.MoveGenerator.DirectMoveGenerator import Ball,Pocket
import threading

class TableManager:
  tables = {}
  count = 0

  def __init__(self):
    pass

  @classmethod
  def new(cls,sim_result):
    cls.count += 1
    cls.tables[cls.count] = Table(cls.count,sim_result)
    return cls.tables[cls.count]

class Table:
  height = 0.54
  half_width_inner = 8.875
  half_width_outer = 9.85
  half_length_inner = 18.775
  half_length_outer = 19.7
  half_mid_width = (half_width_inner+half_width_outer)/2
  P1 = (((half_width_inner+half_width_outer)/2),((half_length_inner+half_length_outer)/2))
  P2 = (half_mid_width,0)
  pockets = [Pocket(P1),
             Pocket(P2),
             Pocket((P1[0],-1*P1[1])),
             Pocket((-1*P1[0],-1*P1[1])),
             Pocket((-1*P2[0],P2[1])),
             Pocket((-1*P1[0],P1[1]))
            ]

  def __init__(self,table_id,sim_result):
    self.table_id = table_id
    self.balls = {}
    for balldata in sim_result:
      if balldata['BallName']!="CueBall":
        self.balls[balldata['BallName']] = Ball(balldata['BallName'],balldata['x'],balldata['z'])
      else:
        self.cue = Ball(balldata['BallName'],balldata['x'],balldata['z'])

  def __repr__(self):
    return f'balls:{self.balls},cue:{self.cue},table_id:{self.table_id}'

  
