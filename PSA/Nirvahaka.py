try:
	import threading
	from Ipc.PipeLine import PipeLine
	from TableManager import Table
	from GameTree import GameTree,GameState
	from GameTable import GameTable
	from PrePostSim import PreSim,PostSim
	from PickPocket.MoveGenerator.Evaluate import EvalNode,RecursiveEvaluation
	from PickPocket.utils.StopWatch import StopWatch
except:
	from .Ipc.PipeLine import PipeLine
	from .TableManager import Table
	from .GameTree import GameTree,GameState
	from .GameTable import GameTable
	from .PrePostSim import PreSim,PostSim
	from .PickPocket.MoveGenerator.Evaluate import EvalNode
	from .PickPocket.utils.StopWatch import StopWatch

import Ipc.commands as commands
import json
import time

LookAheadDepth = 3
pipeline = PipeLine() 
pipeline.open()
pipeline.WaitForArrival()
gametree = GameTree()
gametable = GameTable()
PreSimTask = PreSim(gametable=gametable)
VectorMath_StopWatch = StopWatch()


def RecvGreetings():
	for msg in pipeline.recvr.RecvAll():
		print(msg)

def CreatePreSimTask(move,table):
	def presim_task():
		gametable.ReserveTable(move)
		cmd = commands.EncodeSGState(table,move)
		pipeline.sender.Send(cmd)
		print(move)
		# print(move.valid,move.pocket,move.shotangle,move.target.BallName,
		# 			move.v,move.target_vel,move.impact_vel,
		# 			move.cMove.min_dst_to_aiming_line,move.cMove.min_dst_to_target_line)
	return presim_task

def CreatePostSimTask():
	def postsim_task(msg,gametable):
		json_text = json.loads(msg)
		move = gametable.MoveOf(json_text['table_no']).move
		gametable.CleanTable(json_text['table_no'])
		move.SimResultNode = GameState.fromSimResult(json_text,parent_node=move.node,branch=move)
		EvalNode(move.SimResultNode)
		if move.SimResultNode.score>0:
			move.node.terminate = False
			pAf_states[move.SimResultNode.depth].append(move.SimResultNode)
		return move.SimResultNode
	return postsim_task



def EnqPreSimTasks(node):
	node.SpawnDirectMoves()
	for move in node.table.moves:
		VectorMath_StopWatch.Start()
		move.CalcShotAngle()
		move.CheckValidity(node.table)
		VectorMath_StopWatch.Stop()
		if move.valid==0:
			PreSimTask.Enq(CreatePreSimTask(move,move.node.table))

def EnqPreSimTasks_V(branch):
	branch.SpawnVStrikes()
	for vstrike in branch.VStrikes:
		PreSimTask.Enq(CreatePreSimTask(vstrike,vstrike.node.table))

def EnqPreSimTasks_VR(branch):
	branch.SpawnVRStrikes()
	for vrstrike in branch.VRStrikes:
		PreSimTask.Enq(CreatePreSimTask(vrstrike,vrstrike.node.table))

def isSimulationRunning():
	return not(gametable.fullhouse_evt.is_set()) or PreSimTask.StartEvent.is_set()

def PlayShot(move):
	enc_msg = commands.EncodeStrike(move)
	print(enc_msg)
	pipeline.sender.Send(enc_msg)
	pipeline.WaitForArrival()
	msg = next(pipeline.recvr.RecvAll())
	print(msg)
	return json.loads(msg)

PostSimTask = PostSim(pipeline=pipeline,task=CreatePostSimTask(),
											gametable=gametable,Expecting_func = isSimulationRunning)

RecvGreetings()
PreSimTask.start()
simresult = PlayShot(gametree.root.table.moves[0])
start_time = time.time()
gametree.root.table.moves[0].SimResultNode = GameState.fromSimResult(simresult,gametree.root,
																																		 gametree.root.table.moves[0],
																																		 depth=0)
gametree.root.RealChild = gametree.root.table.moves[0].SimResultNode
BoardState = gametree.root.RealChild
pAf_states = [gametree.root.table.moves[0].SimResultNode,[],[],[]]

while len(BoardState.table.balls)>0:
	EnqPreSimTasks(BoardState)
	PostSimTask.Restart()  #has to be called after PreSim Tasks have started
	while True:
		if  isSimulationRunning() or  PostSimTask.result_available_evt.is_set():
			result_node = PostSimTask.GetSimResult()
			if result_node.branch.move_type == 'DIRECT_MOVE':
				if result_node.score>0:
					if result_node.depth<LookAheadDepth:
						EnqPreSimTasks(result_node)
					EnqPreSimTasks_V(result_node.branch)
			elif result_node.branch.move_type == 'DIRECT_MOVE_V':
				if result_node.score > 0:
					if result_node.depth<LookAheadDepth:
						EnqPreSimTasks(result_node)
					EnqPreSimTasks_VR(result_node.branch)
			else :
				if result_node.score >0:
					if result_node.depth<LookAheadDepth:
						EnqPreSimTasks(result_node)
		else:
			print('Halting usual main thred tasks')
			gametable.fullhouse_evt.wait()
			print('sim complete')
			BoardState.FindBestMove(LookAheadDepth)
			simresult = PlayShot(BoardState.BestMove)
			BoardState.RealChild = GameState.fromSimResult(simresult,parent_node=BoardState,
																										 branch=BoardState.BestMove,depth=0)
			BoardState = BoardState.RealChild
			pAf_states = [BoardState,[],[],[]]
			print(f'moving to next shot balls remaining {len(BoardState.table.balls)}')
			break

print(f'time taken:{time.time()-start_time}')
print(f'total time waited for game table availability {PostSimTask.stopwatch.elapsed_time_s}')
print(f'time taken by direct move vector math {VectorMath_StopWatch.elapsed_time_s}')

# PostSimTask.stop() have to find a way a stop these threads
# PreSimTask.stop()
# for child in pAf_states[1]:
# 	RecursiveEvaluation(child,LookAheadDepth)
# 	print(f'score:{child.score} target:{child.branch.target.BallName}')


# print(f'{not(gametable.fullhouse_evt.is_set())} {PreSimTask.StartEvent.is_set()} {PostSimTask.result_available_evt.is_set()}')
# for child in pAf_states[1]:
# 	for move in child.table.moves:
# 		if move.SimResultNode:
# 			move.node.score += move.SimResultNode.score
# 	print(f'score:{child.score} target:{child.branch.target.BallName}')

# for move in pAf_states[depth].table.moves:
# 	if move.valid==0:
# 		EvalNode(move.SimResultNode)
# 		if move.SimResultNode.score>0:
# 			move.node.terminate = False
# 			pAf_states[1].append(move.SimResultNode)
# 			EnqPreSimTasks(move.SimResultNode)
# PreSimTask.StopEvent.wait()
# print('pre sim task complete')
# PostSimTask.NodeSimComplete_Event.wait()
# print('sim complete')

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
