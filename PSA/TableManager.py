from PSA.PickPocket.MoveGenerator.DirectMoveGenerator import Ball,Pocket
import threading

class TableManager:
  tables = {}
  count = 0

  def __init__(self):
    pass
  
  @classmethod
  def UpdateTable(cls,table_id,update_msg):
    cls.table[table_id].update_ball_loc(update_msg)

  @classmethod
  def new(cls):
    cls.cnt += 1
    table = Table(cls.cnt)
    cls.tables[cls.cnt] = table

class Table:
  height = 43.941
  half_width_inner = 0.61
  half_width_outer = 0.66
  half_length_inner = 0.128
  half_length_outer = 0.135
  half_mid_width = 0.62
  P1 = (((half_width_inner+half_width_outer)/2),height,((half_length_inner+half_length_outer)/2))
  P2 = (half_mid_width,height,0)
  pockets = [Pocket(P1),
             Pocket(P2),
             Pocket((P1[0],P1[1],-1*P1[2])),
             Pocket((-1*P1[0],P1[1],-1*P1[2])),
             Pocket((-1*P2[0],P2[1],P2[2])),
             Pocket((-1*P1[0],P1[1],P1[2]))
            ]

  def __init__(self,table_id):
    cue = None
    balls = {}
    self.table_id = table_id
  
  def update_ball_loc(self,ball_update_msg):
    if ball_update_msg['BallName'] in self.balls:
      self.balls[ball_update_msg['BallName']].update()
    else:
      self.balls[ball_update_msg['BallName']] = Ball(ball_update_msg['BallName'],ball_update_msg['x'],ball_update_msg['y'],ball_update_msg['z'])
