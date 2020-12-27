from sympy import Point,Line,Segment
import numpy as np
import math


BallRadius = 0.5
PocketRadius = 5
logging = None

class Ball:
  Radius = BallRadius
  Diameter = BallRadius*2
  def __init__(self,BallName,x,z):
    self.BallName = BallName
    self.loc = Point(x,z)

  def __repr__(self):
    return f'Ball({self.BallName},{self.loc})'

class Pocket:
  Radius = PocketRadius
  
  def __init__(self,center):
    self.center = Point(*center)
  
  def __repr__(self):
    return f'Pocket({self.center})'


class Move:
  MIN_AngleOfStrike = np.pi-((86*np.pi)/180)
  GHOSTBALL_CLS_FACTOR = 1
  CONST_P1 = 1.602
  CONST_P2 = 20.49

  def __init__(self,cue=None,pocket=None,target=None):
    self.cue = cue
    self.pocket = pocket
    self.target = target
    self.ghostball = None
    self.target_vec = None
    self.aiming_vec = None
    self.shotangle = None
    self.valid = False
    self.target_vel = 0
    self.v = 0
    self.VStrikes = []
    self.SimResultNode = None
    self.gametable_id = None
    self.a = 0
    self.b = 0
    self.impact_vel = 0
    
  def CalcShotAngle(self):
    shifted_pckt = self.pocket.center-self.target.loc
    self.ghostball = (self.target.loc+self.cue.Diameter*(self.target.loc-self.pocket.center)/self.pocket.center.distance(self.target.loc))
    self.aiming_vec = Segment(self.cue.loc,self.ghostball)
    self.target_vec = Segment(self.pocket.center,self.ghostball)
    self.shotangle = self.aiming_vec.angle_between(self.target_vec).evalf()
    shifted_ghost = self.ghostball-self.cue.loc
    self.aiming_vec_ag = math.atan(shifted_ghost.y/shifted_ghost.x)
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
      self.CalcMinVelocity_reqd()
      return f'hodi tondare illa'
    return 'shotangle not valid'

  @staticmethod
  def signof(x):
    return 1 if x>0 else -1
  
  def CalcMinVelocity_reqd(self):
    self.target_vel = self.CONST_P1*self.target_vec.length+self.CONST_P2##from VDModel
    self.impact_vel = 2*self.target_vel*math.cos(math.pi-self.shotangle)##conservation of momentum in 2D same ball mass ans elastic collission
    self.v = self.impact_vel+(self.CONST_P1*self.aiming_vec.length+self.CONST_P2)

  def SpawnVStrikes(self):
    self.VStrikes = []
    for i in range(abs((VStrike.v_max-self.v)//VStrike.v_step)):
      self.VStrikes.append(VStrike(self.v+i*VStrike.v_step,self.aiming_vec_ag))

  def __repr__(self):
    return ','.join(f'{key}:{value}' for key,value in self.__dict__.items())


class VStrike:
  v_step = 10
  v_max = 250

  def __init__(self,v,phsi):
    self.v = v
    self.a = 0.0
    self.b = 0.0
    self.VRStrikes = []
    self.gametable_id = None
    self.aiming_vec_ag = phsi
    self.SimResultNode = None


  def SpawnVRStrikes(self):
    self.VRStrikes = []
    for i in range(1,VRStrike.a_len):
      for j in range(1,VRStrike.a_len):
        self.VRStrikes.append(VRStrike(self.v,VRStrike.a_min+i*VRStrike.a_step,VRStrike.a_min+j*VRStrike.a_step,self.aiming_vec_ag))

class VRStrike:
  a_step = 0.23
  a_min = 0
  a_len = 3
  
  def __init__(self,v,a,b,phsi):
    self.v = v
    self.a = a
    self.b = b
    self.gametable_id = None
    self.aiming_vec_ag = phsi
    self.SimResultNode = None

    # def CalcShotAngle(self):
  #   shifted_pckt = self.pocket.center-self.target.loc
  #   self.ghostball = (self.target.loc+self.cue.Diameter*(self.target.loc-self.pocket.center)/self.pocket.center.distance(self.target.loc))
  #   self.aiming_vec = Line(self.cue.loc,self.ghostball)
  #   self.target_vec = Line(self.pocket.center,self.ghostball)
  #   self.shotangle = self.aiming_vec.angle_between(self.target_vec).evalf()
  #   shifted_ghost = self.ghostball-self.cue.loc
  #   self.aiming_vec_ag = math.atan(shifted_ghost.y/shifted_ghost.x)
  #   if shifted_ghost.x<0:
  #     self.aiming_vec_ag = math.pi+self.aiming_vec_ag



  # def CheckValidity(self,table):
  #   if self.shotangle>self.MIN_AngleOfStrike:
  #     for ball in table.balls.values():
  #       if ball.BallName!=self.target.BallName:
  #         norm_aiming_line = self.aiming_vec.perpendicular_line(ball.loc)
  #         intersect_norm_aim = norm_aiming_line.intersection(self.aiming_vec)[0]
  #         # check if intersection point lies on aiming_line
  #         dist_cue_ghost = self.cue.loc.distance(self.ghostball)
  #         dist_to_cue = self.cue.loc.distance(intersect_norm_aim)
  #         dist_to_ghost = self.ghostball.distance(intersect_norm_aim)
  #         if (dist_to_cue>dist_cue_ghost) or (dist_to_ghost > dist_cue_ghost):
  #           min_dst_to_aiming_line = 0 #doesnt affect ball movement
  #         else:
  #           min_dst_to_aiming_line = intersect_norm_aim.distance(ball.loc)
  #           if min_dst_to_aiming_line <ball.Diameter:
  #             self.valid = False
  #             return f'{ball.BallName} adda ide'
  #         norm_target_line = self.target_vec.perpendicular_line(ball.loc)
  #         intersect_norm_target = norm_target_line.intersection(self.target_vec)[0]
  #         # check if intersection point lies on target_line
  #         dist_pocket_ghost = self.pocket.center.distance(self.ghostball)
  #         dist_to_pocket = self.pocket.center.distance(intersect_norm_target)
  #         dist_to_ghost = self.ghostball.distance(intersect_norm_target)
  #         if (dist_to_pocket>dist_pocket_ghost) or (dist_to_ghost > dist_pocket_ghost):
  #           min_dst_to_target_line = 0
  #         else:
  #           min_dst_to_target_line = intersect_norm_target.distance(ball.loc)
  #           if min_dst_to_target_line < ball.Diameter:
  #             self.valid = False
  #             return f'{ball.BallName} adda ide'
  #     self.valid = True
  #     return f'hodi tondare illa'
  #   return 'shotangle not valid'
