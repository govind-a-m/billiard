from sympy import Point,Segment
import numpy as np
import math

BallRadius = 0.5
PocketRadius = 5



class Ball:
  Radius = BallRadius
  Diameter = BallRadius*2
  def __init__(self,BallName,x,y,z):
    self.BallName = BallName
    self.loc = Point(x,y,z)

  def __repr__(self):
    return f'Ball({self.BallName},{self.loc})'

class Pocket:
  Radius = PocketRadius
  
  def __init__(self,center):
    self.center = Point(*center)
  
  def __repr__(self):
    return f'Pocket({self.center})'


class Strike:
  MIN_AngleOfStrike = np.pi-((86*np.pi)/180)
  GHOSTBALL_CLS_FACTOR = 1
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
    shifted_pckt = self.pocket.center-self.target.loc
    self.ghostball = (self.target.loc+self.cue.Diameter*(self.target.loc-self.pocket.center)/self.pocket.center.distance(self.target.loc)).evalf()
    self.aiming_vec = Segment(self.cue.loc,self.ghostball)
    self.target_vec = Segment(self.pocket.center,self.ghostball)
    self.shotangle = self.aiming_vec.angle_between(self.target_vec).evalf()
    shifted_ghost = self.ghostball-self.cue.loc
    self.aiming_vec_ag = math.atan(shifted_ghost.z/shifted_ghost.x)
    if shifted_ghost.x<0:
      self.aiming_vec_ag = math.pi+self.aiming_vec_ag



  def CheckValidity(self,table):
    if self.shotangle>self.MIN_AngleOfStrike:
      for ball in table.balls.values():
        if ball.BallName!=self.target.BallName:
          min_dst_to_aiming_line = self.aiming_vec.perpendicular_segment(ball.loc).length.evalf()
          min_dst_to_target_line = self.target_vec.perpendicular_segment(ball.loc).length.evalf()
          if min_dst_to_aiming_line<ball.Diameter or min_dst_to_target_line<ball.Diameter:
            self.valid = False
            return f'{ball.BallName} adda ide'
      self.valid = True
      return f'hodi tondare illa'
    return 'shotangle not valid'

  @staticmethod
  def signof(x):
    return 1 if x>0 else -1
  
  def __repr__(self):
    return ','.join(f'{key}:{value}' for key,value in self.__dict__.items())


def GenMoves(table):
  for target in table.balls.values():
    for pocket in table.pockets:
      strike = Strike(table.cue,pocket,target)
      yield strike

