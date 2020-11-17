import json
import pandas as pd

class Ball:
  
  def __init__(self,name,x=None,y=None,z=None):
    self.name = name
    self.x = x
    self.y = y
    self.z = z
    self.timestamp = None
    setattr(self.__class__,

  def UpdatePosition(msg):
    update_data = json.loads(msg)
    self.x = update_data[x]
    self.y = update_data[y]
    self.z = update_data[z]
    self.timestamp = update_data[timestamp]
  