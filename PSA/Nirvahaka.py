try:
	from Ipc.PipeLine import PipeLine
	from TableManager import Table
	from GameTree import GameTree,GameState
	from GameTable import GameTable
	from PrePostSim import PreSim,PostSim
except:
	from .Ipc.PipeLine import PipeLine
	from .TableManager import Table
	from .GameTree import GameTree,GameState
	from .GameTable import GameTable
	from .PrePostSim import PreSim,PostSim

import threading
import Ipc.commands as commands
import time
import json


		

pipeline = PipeLine() 
pipeline.open()
pipeline.WaitForArrival()
gametree = GameTree()
gametable = GameTable()
PreSimTask = PreSim()

def RecvGreetings():
	for msg in pipeline.recvr.RecvAll():
		print(msg)

def CreatePresimTask(move,table):
	def presim_task():
		move.CalcShotAngle()
		move.CheckValidity(table)
		if move.valid==0:
			gametable.ReserveTable(move)
			cmd = commands.EncodeSGState(table,move)
			pipeline.sender.Send(cmd)
			print(move.valid,move.pocket,move.shotangle,move.target.BallName,
						move.v,move.target_vel,move.impact_vel,
						move.cMove.min_dst_to_aiming_line,move.cMove.min_dst_to_target_line)
	return presim_task

def CreatePostSimTask():
	def postsim_task(msg,gametable):
		json_text = json.loads(msg)
		move = gametable.MoveOf(json_text['table_no']).move
		gametable.CleanTable(json_text['table_no'])
		move.SimResultNode = GameState.fromSimResult(json_text,parent_node=move.node,branch=move)
	return postsim_task

PostSimTask = PostSim(pipeline=pipeline,task=CreatePostSimTask(),gametable=gametable)

RecvGreetings()
PreSimTask.start()
enc_msg = commands.EncodeStrike(gametree.root.table.moves[0])
print(enc_msg)
pipeline.sender.Send(enc_msg)
pipeline.WaitForArrival()
msg = next(pipeline.recvr.RecvAll())
print(msg)
simresult = json.loads(msg)
gametree.root.table.moves[0].SimResultNode = GameState.fromSimResult(simresult,gametree.root,gametree.root.table.moves[0])
gametree.root.table.moves[0].SimResultNode.SpawnDirectMoves()
pAf_states = [gametree.root,gametree.root.table.moves[0].SimResultNode,None,None]
depth = 1
width = 0
for move in pAf_states[depth].table.moves:
	PreSimTask.Enq(CreatePresimTask(move,move.node.table))
PostSimTask.start()
PreSimTask.StopEvent.wait()
print('pre sim task complete')
PostSimTask.NodeSimComplete_Event.wait()
print('sim complete')
# pipeline.WaitForArrival()
# for msg in pipeline.recvr.RecvAll():
# 	print(msg)

# pipeline.sender.Send(commands.StrikeCmd(1, 300, 1.570796, 0, 0))
# def GetTabledata():
# 	nof_recvd_msg = 0
# 	for i in range(100):
# 		time.sleep(1)
# 		for msg in pipeline.recvr.RecvAll():
# 			print(msg)
# 			nof_recvd_msg += 1
# 			if(nof_recvd_msg == 2):
# 				return msg


# msg = GetTabledata()
# with open('table.txt', 'w') as f:
# 	f.write(msg)
# tabledata = json.loads(msg)['balls']
# table = TableManager.new(tabledata)
# strikes = []
# for strike in GenMoves(table):
# 	strike.CalcShotAngle()
# 	print(strike.shotangle,strike.CheckValidity(table),strike.pocket.center,strike.target.BallName)
# 	strikes.append(strike)
# for strike in strikes:
# 	if strike.valid:
# 		print(strike.target.BallName,strike.target.loc,strike.ghostball)
# 		pipeline.sender.Send(commands.StrikeCmd(1, 75, float(strike.aiming_vec_ag), 0, 0))
# pipeline.WaitForArrival()
# print(pipeline.recvr.RecvOne())



# pipeline.WaitForArrival()
# print(table)
# with open('table.tbl','w') as f:
#   pickle.dump(table,f)
