import json

def ConvertTobytes(cmd):
  return (json.dumps(cmd)+'END_OF_MSG').encode('ascii','replace')

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

