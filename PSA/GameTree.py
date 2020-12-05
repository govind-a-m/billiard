from PickPocket.MoveGenerator.DirectMoveGenerator import Move,VStrike,VRStrike
from sympy import Segment,Point,Line
import math
import Ipc.commands as commands

starting_shot = Move()
starting_shot.aiming_vec_ag = math.pi/2
starting_shot.v = 500
starting_shot.gametable_id = 0

class GameTree:

  def __init__(self):
    self.root = GameState()
    self.root.moves = [starting_shot]


class GameState:

  def __init__(self,table=None,gametable=None,parent=None):
    self.node = table
    self.gametable = gametable
    self.stage = "INIT"
    self.moves = []
    self.parent = None


