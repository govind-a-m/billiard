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
  public static Dictionary<int,TableManager> tables = new Dictionary<int, TableManager>(); 

  void Awake()
  {
    fc = new ForceCommand(0.0f, 0.0f, 0.0f, 0.0f,0);
    pipeline = new ProcessPipeline();
    pipeline.StartPipeLine();
  }

  void Update()
  {
    // foreach(String msg in pipeline.RecvAll())
		// {

		// 	String msg_type =  msg.Substring(0,10);
    //   Debug.Log("recieved msg"+msg);
    //   switch(msg_type)
    //   {
    //     case "STRIKE_CMD":

    //       break;

    //   }
    //   if(msg_type == "STRIKE_CMD")
    //   {

    //   }
		// }
  }

  private void PassOnStrikeCmd(String msg)
  {
    fc = ForceCommand.getFc(msg);
    if(fc.F>0.0f)
    {
      tables[0].Fc = fc;
      tables[0].enabled = true;
    }
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
