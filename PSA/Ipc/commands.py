import json

def ConvertTobytes(header,cmd,footer):
  return (header+json.dumps(cmd)+footer).encode('ascii','replace')

def NewTableCmd(x,z,table_id):
  cmd = {
          'CMD_ID':'NEW_TABLE',
          'PARAMS':{
                    'x':x,
                     'y':z,
                     'table_id':table_id
                    }
          }
  return ConvertTobytes(cmd)



def StrikeCmd(table_id,force,phsi,a,b):
  cmd = {
          'F' : force,
          'phsi' : phsi,
          'a' : 0,
          'b' : 0,
          'table_id':table_id
        }
  return ConvertTobytes('STRIKE_CMD',cmd,'END_OF_MSG')

def EncodeStrike(strike):
  return StrikeCmd(strike.gametable_id,strike.v,strike.aiming_vec_ag,strike.a,strike.b)

def EncodeSGState(table,strike):
  balls = []
  for ball in table.balls.values():
    balls.append({"BallName":ball.BallName,"x":float(ball.x),"z":float(ball.y)})
  balls.append({"BallName":table.cue.BallName,"x":float(table.cue.x),"z":float(table.cue.y)})
  cmd = {
          "balls" : balls,
          "force" : {
                      'F' : float(strike.v),
                      'phsi' : float(strike.aiming_vec_ag),
                      'a' : strike.a,
                      'b' : strike.b,
                      'table_id':strike.gametable_id
                    }
        }
  return ConvertTobytes('RST_STRIKE',cmd,'END_OF_MSG')