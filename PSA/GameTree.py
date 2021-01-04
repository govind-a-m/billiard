
import math
try:
  from PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
  from TableManager import Table
  from PickPocket.MoveGenerator.Evaluate import RecursiveEvaluation
except:
  from .PickPocket.MoveGenerator.DirectMoves import Move,VRStrike,VStrike
  from .TableManager import Table
  from .PickPocket.MoveGenerator.Evaluate import RecursiveEvaluation

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
    self.root = GameState(table=root_table,depth=-1)
    self.root.table.moves[0].node = self.root

class GameState:

  def __init__(self,table=None,parent_node=None,branch=None,depth=None):
    self.table = table
    self.stage = "INIT"
    self.parent = parent_node
    self.branch = branch
    self.BestMove = None
    self.score = None
    self.terminate = True
    if depth==None:    
      self.depth = parent_node.depth+1
    else:
      self.depth = depth
    self.RealChild = None

  @classmethod
  def fromSimResult(cls,simresult,parent_node,branch,depth=None):
    return cls(table=Table(sim_result=simresult['balls']),parent_node=parent_node,
               branch=branch,depth=depth)    

  def SpawnDirectMoves(self):
    self.table.moves = []
    for target in self.table.balls.values():
      for pocket in self.table.pockets:
        move =  Move(self.table.cue,pocket,target,node=self)
        self.table.moves.append(move)
  
  def FindBestMove(self,look_ahead_depth):
    best_score = 0
    for move in self.table.moves:
      if (move.SimResultNode is not None) and (move.valid==0):
        RecursiveEvaluation(move.SimResultNode,depth=look_ahead_depth)
        best_score = self.assign_best_move(best_score,move)
        for vstrike in move.VStrikes:
          RecursiveEvaluation(vstrike.SimResultNode,depth=look_ahead_depth)
          best_score = self.assign_best_move(best_score,vstrike)
          for vrstrike in vstrike.VRStrikes:
            RecursiveEvaluation(vrstrike.SimResultNode,depth=look_ahead_depth)
            best_score = self.assign_best_move(best_score,vrstrike)
    print(f'best score:{self.BestMove.SimResultNode.score} move:{self.BestMove}') 
    return self.BestMove


  def assign_best_move(self,best_score,move):
    if move.SimResultNode.score>best_score:
      self.BestMove = move
      return move.SimResultNode.score
    return best_score
