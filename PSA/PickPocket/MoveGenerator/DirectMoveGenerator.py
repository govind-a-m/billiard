from sympy import Point,Segment
import numpy as np

BallRadius = 0.5
PocketRadius = 5

class Table:
  height = 43.941
  half_width_inner = 0.61
  half_width_outer = 0.66
  half_length_inner = 0.128
  half_length_outer = 0.135
  half_mid_width = 0.62

  def __init__(self,x,z,table_id):
    cue = None
    balls = {}
    self.x = x
    self.z = z
    self.table_id = table_id
    P1 = (((half_width_inner+half_width_outer)/2)+x,height,((half_length_inner+half_length_outer)/2)+y)
    P2 = (half_mid_width+x,height,z)
    Pockets = [Pocket(P1),
               Pocket(P2),
               Pocket((P1[0],P1[1],-1*P1[2])),
               Pocket((-1*P1[0],P1[1],-1*P1[2])),
               Pocket((-1*P2[0],P2[1],P2[2])),
               Pocket((-1*P1[0],P1[1],P1[2]))
              ]

  
  def update_ball_loc(self,ball_update_msg):
    if ball_update_msg['BallName'] in self.balls:
      self.balls[ball_update_msg['BallName']].update()
    else:
      self.balls[ball_update_msg['BallName']] = Ball(ball_update_msg['BallName'],ball_update_msg['x'],ball_update_msg['y'],ball_update_msg['z'])


class Ball:
  Radius = BallRadius
  Diameter = BallRadius*2
  def __init__(self,name,x,y,z):
    self.name = name
    self.loc = Point(x,y,z)

  def update(self,loc_data):
    self.loc.x = loc_data['x']
    self.loc.y = loc_data['y']
    self.loc.z = loc_data['z']

class Pocket:
  Radius = PocketRadius
  
  def __init__(self,center):
    center = Point(*center)


class Strike:
  signof = lambda x:float(np.sign(x))
  MIN_AngleOfStrike = np.pi-((82*np.pi)/180)

  def __init__(self,cue=None,pocket=None,target=None):
    self.cue = cue
    self.pocket = pocket
    self.target = target
    self.ghostball = None
    self.target_vec = None
    self.aiming_vec = None
    self.shotangle = None
    self.valid = False

  def CalcShotAngle(self):
    self.target_vec = Segment(pocket.center,self.cue)
    self.ghostball = self.target+Point3D(-2*self.cue.Radius*self.signof(self.signof(self.target.x)),self.target.y,-2*self.cue.Radius*self.signof(self.signof(self.target.z)))
    self.aiming_vec = Segment(self.cue,self.ghostball)
    self.shotangle = self.aiming_vec.angle_between(self.target_vec).evalf()
    self.shotangle = None

  
  def CheckValidity(self,table):
    if self.shotangle>MIN_AngleOfStrike:
      for ball in table.balls:
        min_dst_to_aiming_line = self.aiming_vec.perpendicular_segment(ball.loc).length.evalf()
        min_dst_to_target_line = self.target_vec.perpendicular_segment(ball.loc).length.evalf()
        if min_dst_to_aiming_line<ball.Diameter or min_dst_to_target_line<ball.Diameter:
          self.valid = False
          return f'{ball.name} adda ide'
      self.valid = True
      return f'hodi tondare illa'
    return 'shotangle not valid'



def GenMoves(table):
  for target in table.balls:
    for pocket in table.pockets:
      strike = Strike(table.cue,pocket,target)
      yield strike

