using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using SerializeData;

public class GameProcess : MonoBehaviour
{
  public static ProcessPipeline pipeline;
  private static int _NofRecvdMsgs { get; }
  public ForceCommand fc;
  public SimGameState simGameState;
  public static int TotalNofTables = 40;
  public static TableManager[] tables = new TableManager[TotalNofTables];

  void Awake()
  {
    fc = new ForceCommand(0.0f, 0.0f, 0.0f, 0.0f,0);
    pipeline = new ProcessPipeline();
    pipeline.StartPipeLine();
    //SimGameState.jsonprototype();
  }

  void Update()
  {
    foreach(String msg in pipeline.RecvAll())
		{

			String msg_type =  msg.Substring(0,10);
      Debug.Log("recieved msg"+msg);
      switch(msg_type)
      {
        case "STRIKE_CMD":
          PassOnStrikeCmd(msg.Substring(10));
          break;
        case "RST_STRIKE":
          RST_Strike_Cmd(msg.Substring(10));
          break;
      }
		}
  }

  private void PassOnStrikeCmd(String msg)
  {
    fc = ForceCommand.getFc(msg);
    if(fc.F>0.0f)
    {
      tables[fc.table_id].Fc = fc;
      tables[fc.table_id].enabled = true;
    }
  }

  private void RST_Strike_Cmd(String msg)
  {
    simGameState = SimGameState.get_SGState(msg);
    tables[simGameState.force.table_id].SetTable(simGameState.balls);
    tables[simGameState.force.table_id].Fc = simGameState.force;
    tables[simGameState.force.table_id].enabled = true;
  }


  private void OnDestroy()
  {
    pipeline.EndSendThread();
  }

  public static int NofRecvdMsgs
  {
    get { return pipeline.recvQ.Q.Count;}
  }
}
