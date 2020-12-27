
import math
try:
  from PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
  from TableManager import Table
except:
  from .PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
  from .TableManager import Table

import Ipc.commands as commands
import json

class GameTree:

  def __init__(self,force_vel=500,table_id=0):
    starting_shot = Move()
    starting_shot.aiming_vec_ag = math.pi/2
    starting_shot.gametable_id = 0
    starting_shot.v = force_vel
    root_table = Table(None)
    root_table.moves = [starting_shot]
    self.root = GameState(table=root_table)
    self.root.table.moves[0].node = self.root

class GameState:

  def __init__(self,table=None,parent_node=None,branch=None):
    self.table = table
    self.stage = "INIT"
    self.parent = parent_node
    self.branch = branch
    self.BestScore = None
    self.BestMove = None
    

  @classmethod
  def fromSimResult(cls,simresult,parent_node,branch):
    return cls(table=Table(sim_result=simresult['balls']),parent_node=parent_node,
               branch=branch)    

  def SpawnDirectMoves(self):
    self.table.moves = []
    for target in self.table.balls.values():
      for pocket in self.table.pockets:
        move =  Move(self.table.cue,pocket,target,node=self)
        self.table.moves.append(move)