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

