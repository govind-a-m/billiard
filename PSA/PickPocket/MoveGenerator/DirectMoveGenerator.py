from sympy import Point,Segment
import numpy as np

BallRadius = 0.5
PocketRadius = 5



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
    self.ghostball = self.target+Point(-2*self.cue.Radius*self.signof(self.signof(self.target.x)),self.target.y,-2*self.cue.Radius*self.signof(self.signof(self.target.z)))
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

