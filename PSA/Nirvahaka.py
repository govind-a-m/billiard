from .Ipc.PipeLine import PipeLine,commands
from .TableManager import TableManager
import threading

table = TableManager.new()
pipeline = PipeLine()
pipeline.sender.Send(commands.StrikeCmd(table.table_id,100,1.570796,0,0))

while True:
  try:
    pipeline.WaitForArrival()
    for msg in pipeline.recvr.RecvAll():
      ##handle recieved messages
      pass
