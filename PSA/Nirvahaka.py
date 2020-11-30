from Ipc.PipeLine import PipeLine
import Ipc.commands as commands
from TableManager import TableManager
import threading
import pickle
from PickPocket.MoveGenerator.DirectMoveGenerator import Move, GenMoves
import time
import json

pipeline = PipeLine()
pipeline.open()
pipeline.sender.Send(commands.StrikeCmd(1, 300, 1.570796, 0, 0))


def GetTabledata():
	nof_recvd_msg = 0
	for i in range(100):
		time.sleep(1)
		for msg in pipeline.recvr.RecvAll():
			print(msg)
			nof_recvd_msg += 1
			if(nof_recvd_msg == 2):
				return msg


msg = GetTabledata()
with open('table.txt', 'w') as f:
	f.write(msg)
tabledata = json.loads(msg)['balls']
table = TableManager.new(tabledata)
strikes = []
for strike in GenMoves(table):
	strike.CalcShotAngle()
	print(strike.shotangle,strike.CheckValidity(table),strike.pocket.center,strike.target.BallName)
	strikes.append(strike)
for strike in strikes:
	if strike.valid:
		print(strike.target.BallName,strike.target.loc,strike.ghostball)
		pipeline.sender.Send(commands.StrikeCmd(1, 75, float(strike.aiming_vec_ag), 0, 0))
pipeline.WaitForArrival()
print(pipeline.recvr.RecvOne())



# pipeline.WaitForArrival()
# print(table)
# with open('table.tbl','w') as f:
#   pickle.dump(table,f)
