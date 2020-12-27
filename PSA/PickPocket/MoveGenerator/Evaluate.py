Nof_Balls = 6

def eval(node):
  for move in node.table.moves:
    pass

def successfull(move):
  if len(move.node.parent_node.table.balls)>len(move.node.table.balls):
    return True
  return False