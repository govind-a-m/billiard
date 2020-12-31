Nof_Balls = 6

def eval(node):
  for move in node.table.moves:
    pass

def successfull(move):
  if len(move.node.parent.table.balls)>len(move.node.table.balls):
    return True
  return False


def EvalNode(node):
  '''
  Evaluates node
  as there is no error introduced to shots its simple now
  '''
  node.score = len(node.parent.table.balls)-len(node.table.balls)

def RecursiveEvaluation(node,depth):
  if node==None:
    return 0
  if node.depth==depth:
    return node.score
  else:
    for move in node.table.moves:
      if move.valid==0:
        node.score += RecursiveEvaluation(move.SimResultNode,depth)
        for vstrike in move.VStrikes:
          node.score += RecursiveEvaluation(vstrike.SimResultNode,depth)
          for vrstrike in vstrike.VRStrikes:
            node.score += RecursiveEvaluation(vrstrike.SimResultNode,depth)
    return node.score
