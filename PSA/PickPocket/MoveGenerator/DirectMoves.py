from ctypes import *
import ctypes

DirMov = ctypes.CDLL.LoadLibrary('DirectMoves.so');

class cPoint(ctypes.Structure):

  _fields_ = [('x',ctypes.c_double),
              ('y',ctypes.c_double)]

class cBall(ctypes.Structure):

  _fields_ = [('ballidx',ctypes.c_int),
              ('position',cPoint),
              ('valid',c_bool)
              ]



class cVector(ctypes.Structure):
  _fields_ = [('x',c_double),
              ('y',c_double)
             ]


class cSegment(ctypes.Structure):

  _fields_ = [('from',cPoint),
              ('to',cPoint),
              ('vec',cVector),
              ('length',c_double)
             ]



class cMove(ctypes.Structure):
  _fields_ = [('cue',cBall),
              ('pocket',cPoint),
              ('target',cBall),
              ('ghostball',cPoint),
              ('target_vec',cSegment),
              ('aiming_vec',cSegment),
              ('shotangle',c_double),
              ('valid',c_int),
              ('target_vel',c_double),
              ('v',c_double),
              ('impact_vel',c_double),
              ('aiming_vec_ag',c_double)
             ]



class Ball(cBall):
  def __init__(self,BallName,x,y):
    cBall.__init__(self,int(BallName[-1]),cPoint(x,y))
    self.BallName = BallName


class Move(cMove):
   def __init__(self,cue=None,pocket=None,target=None):
    cMove.__init__()
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
    self.SimResultTable = None
    self.gametable_id = None
    self.a = 0
    self.b = 0
    self.impact_vel = 0
