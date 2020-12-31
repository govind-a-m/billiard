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
  public int Nof_RST_Strikes = 0;
  public int Nof_Strikes = 0;

  void Awake()
  {
    fc = new ForceCommand(0.0f, 0.0f, 0.0f, 0.0f,0);
    pipeline = new ProcessPipeline();
    pipeline.StartPipeLine();
    //SimGameState.jsonprototype();
  }

  void Update()
  { 
    // shot_variation_sim();
    // enabled = false;
    foreach(String msg in pipeline.RecvAll())
		{

			String msg_type =  msg.Substring(0,10);
      Debug.Log("recieved msg"+msg);
      switch(msg_type)
      {
        case "STRIKE_CMD":
          PassOnStrikeCmd(msg.Substring(10));
          Nof_Strikes++;
          break;
        case "RST_STRIKE":
          RST_Strike_Cmd(msg.Substring(10));
          Nof_RST_Strikes++;
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

  private void shot_variation_sim()
  { float start_v = 300.0f;
    float step_v = 100.0f;
    int len_v = 4;
    float start_a = 0;
    float step_a = 0.23f;
    int len_a = 3;
    int tno = 0;

    for(int i=0;i<len_v;i++)
    {
      for(int j=0; j<len_a;j++)
      {
        for(int k=0; k<len_a;k++)
        {
          tables[tno].Fc = new ForceCommand(start_v+i*step_v,1.57f,start_a+step_a*j,start_a+step_a*k,tno);
          tables[tno].enabled = true;
          tno++;
        }
      }
    }
    return;
  }
}
