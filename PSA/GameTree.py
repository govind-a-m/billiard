from sympy import Segment,Point,Line
import math
try:
  from PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
except:
  from .PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
import Ipc.commands as commands

starting_shot = Move()
starting_shot.aiming_vec_ag = math.pi/2
starting_shot.v = 300
starting_shot.gametable_id = 0


class GameTree:

  def __init__(self,force_vel=500,table_id=0):
    self.root = GameState()
    starting_shot.v = force_vel
    starting_shot.gametable_id = table_id
    self.root.moves = [starting_shot]

class GameState:

  def __init__(self,table=None,gametable=None,parent=None):
    self.node = table
    self.gametable = gametable
    self.stage = "INIT"
    self.moves = []
    self.parent = None


