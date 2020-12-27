try:
  from PickPocket.MoveGenerator.DirectMoves import Ball,pocket,Move
except:
  from .PickPocket.MoveGenerator.DirectMoves import Ball,pocket,Move

class Table:
  height = 0.54
  half_width_inner = 8.875
  half_width_outer = 9.85
  half_length_inner = 18.775
  half_length_outer = 19.7
  half_mid_width = (half_width_inner+half_width_outer)/2
  P1 = (((half_width_inner+half_width_outer)/2),((half_length_inner+half_length_outer)/2))
  P2 = (half_mid_width,0)
  pockets = [pocket(*P1),
             pocket(*P2),
             pocket(P1[0],-1*P1[1]),
             pocket(-1*P1[0],-1*P1[1]),
             pocket(-1*P2[0],P2[1]),
             pocket(-1*P1[0],P1[1])
            ]
  
  def __init__(self,sim_result):
    self.balls = {}
    self.moves = []
    try:
      for balldata in sim_result:
        if balldata['BallName']!="CueBall":
          self.balls[balldata['BallName']] = Ball(balldata['BallName'],balldata['x'],balldata['z'])
        else:
          self.cue = Ball(balldata['BallName'],balldata['x'],balldata['z'])
    except:
      print('NoneType Simulation result')



  def __repr__(self):
    return f'balls:{self.balls},cue:{self.cue},table_id:{self.table_id}'

  
