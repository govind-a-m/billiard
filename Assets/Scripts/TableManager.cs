using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using SoftwareTimer;
using SQ;
using SerializeData;
using System.Text;
using System;

public class TableManager : MonoBehaviour
{
  public List<BallData> TableData;
  public Dictionary<String,Rigidbody> rbBalls = new Dictionary<string, Rigidbody>();
  public static ProcessPipeline Gp;
  private Transform[] ts;
  public float MAX_NetVelocity = 0.1f;
  private float netvel = 0.0f;
  public Timer timer;
  private BallData ballData;
  public SQEle MsgTemplate;
  public float WaitTimeVel = 0.1f;
  public ForceCommand Fc;
  public int TableNo = 0;
  public CueController cueController;
  public SerializableTableData serializable_tabledata;
  public float posball_y;
  private Vector3 TablePosition;

  void Awake()
  {
    TableData = new List<BallData>();
    serializable_tabledata = new SerializableTableData(TableData);
    MsgTemplate = new SQEle(ConvToBytes(), DefaultCallback);
    enabled = false;
    timer = new Timer(WaitTimeVel);
    cueController = gameObject.transform.Find("CueBall").GetComponent<CueController>();
    ballData = new BallData("init", Vector3.zero);
    foreach(Rigidbody rb in gameObject.GetComponentsInChildren<Rigidbody>())
    {
      rbBalls.Add(rb.gameObject.name,rb);
    }
    posball_y = rbBalls["CueBall"].position.y;
    var tableno_str = gameObject.transform.parent.name.Split('_')[1];
    GameProcess.tables[int.Parse(tableno_str)-1] = this;
    TablePosition = gameObject.transform.parent.transform.position;
    TablePosition.y += posball_y;
    //UnityEngine.Debug.Log(GameProcess.tables[0]);
  }



  void FixedUpdate()
  {
    netvel = 0.0f;
    foreach (Rigidbody rb in rbBalls.Values)
    {
      netvel = netvel + rb.velocity.magnitude;
    }

    if (netvel < MAX_NetVelocity)
    {
      if (timer.status == "STARTED")
      {
        if (timer.Expired(Time.deltaTime))
        {
          TableData.Clear();
          foreach (Rigidbody rb in rbBalls.Values)
          { 
            if(rb.gameObject.activeSelf)
            {
              TableData.Add(new BallData(rb.gameObject.name, rb.position-TablePosition));
            }
            else
            {
              TableData.Add(new BallData(rb.gameObject.name, new Vector3(9999.0F,0.0F,9999.0F)));
            }
            
          }
          MsgTemplate.data = ConvToBytes();
          GameProcess.pipeline.sendQ.Enq(MsgTemplate);
          enabled = false;
          timer.ResetTimer();
        }
      }
      else
      {
        timer.Start();
      }
    }
    else
    {
      timer.ResetTimer();
    }
  }

  public void SetTable(List<BallData> balls)
  { 
    foreach(Rigidbody rb in rbBalls.Values)
    {
      rb.gameObject.SetActive(false);
    }
    foreach(BallData ball in balls)
    {
      rbBalls[ball.BallName].gameObject.SetActive(true);
      rbBalls[ball.BallName].position = new Vector3(ball.x,0.0f,ball.z)+TablePosition;
    }
  }

  private void OnEnable()
  { 
    cueController.ApplyForce(Fc);
    // if(cueController.SimComplete)
    // {
    //   cueController.ApplyForce(Fc);
    // }
    // else
    // {
    //   UnityEngine.Debug.Log("sim not complete");
    // }
  }
  private String SerializeTableData()
  {
    return JsonUtility.ToJson(TableData);
  }

  private byte[] ConvToBytes()
  {
    serializable_tabledata.balls = TableData;
    UnityEngine.Debug.Log(JsonUtility.ToJson(serializable_tabledata) + "END_OF_MSG");
    return Encoding.ASCII.GetBytes(JsonUtility.ToJson(serializable_tabledata) + "END_OF_MSG");
  }

  public void DefaultCallback()
  {

  }

}

