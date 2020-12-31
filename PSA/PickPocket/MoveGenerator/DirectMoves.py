
import ctypes

try:
  DirMov = ctypes.cdll.LoadLibrary(r'.\PSA\PickPocket\MoveGenerator\DirectMoves.so')
except:
  DirMov = ctypes.cdll.LoadLibrary(r'.\PickPocket\MoveGenerator\DirectMoves.so')



class cPoint(ctypes.Structure):

  _fields_ = [('x',ctypes.c_double),
              ('y',ctypes.c_double)]


class Point:
  def __init__(self,cpoint):
    self.cPoint = cpoint
    self.x = cpoint.x.value
    self.y = cpoint.y.value



class cVector(ctypes.Structure):
  _fields_ = [('x',ctypes.c_double),
              ('y',ctypes.c_double)
             ]


class cSegment(ctypes.Structure):

  _fields_ = [('from',cPoint),
              ('to',cPoint),
              ('vec',cVector),
              ('length',ctypes.c_double)
             ]


class pocket:
  def __init__(self,x,y):
    self.cPoint = cPoint(x,y)
    self.x = x
    self.y = y

  def __repr__(self):
    return f'pocket-{self.x},{self.y}'

class cBall(ctypes.Structure):

  _fields_ = [('ballidx',ctypes.c_int),
              ('position',cPoint),
              ]



class Ball:
  def __init__(self,BallName,x,y):
    if BallName!='CueBall':
      self.cBall = cBall(int(BallName[-1]),cPoint(x,y))
    else:
      self.cBall = cBall(0,cPoint(x,y))   
    self.BallName = BallName
    self.x = x
    self.y = y

  def __repr__(self):
    return f'{self.BallName}-x:{self.x},y:{self.y}'

  

class cMove(ctypes.Structure):
  _fields_ = [('cue',cBall),
              ('pocket',cPoint),
              ('target',cBall),
              ('ghostball',cPoint),
              ('target_vec',cSegment),
              ('aiming_vec',cSegment),
              ('shotangle',ctypes.c_double),
              ('valid',ctypes.c_ulong),
              ('target_vel',ctypes.c_double),
              ('v',ctypes.c_double),
              ('impact_vel',ctypes.c_double),
              ('aiming_vec_ag',ctypes.c_double),
              ('min_dst_to_aiming_line',ctypes.c_double),
              ('min_dst_to_target_line',ctypes.c_double)
             ]

class Move:
  def __init__(self,cue=None,pocket=None,target=None,node=None):
    try:
      self.cMove = cMove(cue=cue.cBall,pocket=pocket.cPoint,target=target.cBall)
    except:
      self.cMove = None
      print('none values during Move initialisation')
    self.cue = cue
    self.pocket = pocket
    self.target = target
    # self.ghostball = None
    # self.target_vec = None
    # self.aiming_vec = None
    self.shotangle = 0
    self.aiming_vec_ag = 0
    self.valid = None
    self.target_vel = 0 
    self.v = 0
    self.impact_vel = 0
    self.VStrikes = []
    self.SimResultNode = None
    self.gametable_id = None
    self.a = 0
    self.b = 0
    self.node = node
    self.move_type = "DIRECT_MOVE"

  def CalcShotAngle(self):
    DirMov.CalcShotAngle(ctypes.byref(self.cMove))
    self.shotangle = self.cMove.shotangle
    self.aiming_vec_ag = self.cMove.aiming_vec_ag
  
  def CheckValidity(self,table):
    balls = [val.cBall for val in table.balls.values()]
    DirMov.CheckValidity(ctypes.byref(self.cMove),
                          cballs(*balls),
                          ctypes.c_int(int(len(balls))))
    self.valid = self.cMove.valid
    self.CalcMinVelocity_reqd()
    # if self.cMove.valid==10:
    #   self.valid = False
    # else:
    #   if ((self.cMove.min_dst_to_aiming_line<1) | (self.cMove.min_dst_to_target_line<1)):
    #     self.valid = False
    #   else:
    #     self.valid = True
    #     self.CalcMinVelocity_reqd()
  
  def CalcMinVelocity_reqd(self):
    DirMov.CalcMinVelocity_reqd(ctypes.byref(self.cMove))
    self.target_vel = self.cMove.target_vel
    self.impact_vel = self.cMove.impact_vel
    self.v = self.cMove.v


  def ParseValid_id(self):
    if self.valid>0:
      if self.valid>7:
        return 'shotangle invalid'
      else:
        return f'ball {self.valid} adda ide'
    else:
      return 'hodi tondare illa'
      

  def SpawnVStrikes(self):
    self.VStrikes = []
    for i in range(VStrike.v_len):
      vel = self.v+i*VStrike.v_step
      if vel<VStrike.v_max:
        self.VStrikes.append(VStrike(vel,self.aiming_vec_ag,node=self.node))
      else:
        break
  
  def _PerpSegmentLength(self,ball):
    return (PerpSegmentLength(self.cMove.aiming_vec,ball.cBall.position),
            PerpSegmentLength(self.cMove.target_vec,ball.cBall.position))


  def __str__(self):
    return f'D({self.valid})->target_ball:{self.target.BallName},shotangle:{self.aiming_vec_ag} pocket:{self.pocket.x},{self.pocket.y}'

class VStrike:
  v_step = 50
  v_max = 250
  v_len = 2

  def __init__(self,v,phsi,node):
    self.v = v
    self.a = 0.0
    self.b = 0.0
    self.VRStrikes = []
    self.gametable_id = None
    self.aiming_vec_ag = phsi
    self.node = node
    self.move_type = "DIRECT_MOVE_V"
    self.SimResultNode = None
  
  def SpawnVRStrikes(self):
    self.VRStrikes = []
    for i in range(1,VRStrike.a_len):
      for j in range(1,VRStrike.a_len):
        self.VRStrikes.append(VRStrike(self.v,VRStrike.a_min+i*VRStrike.a_step,
                              VRStrike.a_min+j*VRStrike.a_step,self.aiming_vec_ag,self.node))
  
  def __str__(self):
    return f'DV->shotangle:{self.aiming_vec_ag} target_vel:{self.v}'


class VRStrike:
  a_step = 0.4
  a_min = 0
  a_len = 2
  
  def __init__(self,v,a,b,phsi,node):
    self.v = v
    self.a = a
    self.b = b
    self.gametable_id = None
    self.aiming_vec_ag = phsi
    self.node = node
    self.move_type = "DIRECT_MOVE_VR"
    self.SimResultNode = None

  def __str__(self):
    return f'DVR->target_vel:{self.v} , offsets:{self.a},{self.b}'

PerpSegmentLength = DirMov.PerpSegment
PerpSegmentLength.restype = ctypes.c_double
DirMov.CalcShotAngle.argtypes = [ctypes.POINTER(cMove)]
DirMov.CheckValidity.argtypes = [ctypes.POINTER(cMove),ctypes.POINTER(cBall),ctypes.c_int]
DirMov.CalcMinVelocity_reqd.argtypes = [ctypes.POINTER(cMove)]
cballs = cBall*6
