from Ipc.PipeLine import PipeLine,commands
from TableManager import TableManager
import threading

table = TableManager.new()
pipeline = PipeLine()
pipeline.sender.Send(commands.NewTableCmd(0,0,table.table_id))

while True:
  try:
    pipeline.WaitForArrival()
    for msg in pipeline.recvr.RecvAll():
      ##handle recieved messages
      pass
    