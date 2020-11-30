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
  public Rigidbody[] rbBalls;
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


  void Awake()
  {
    TableData = new List<BallData>();
    serializable_tabledata = new SerializableTableData(TableData);
    MsgTemplate = new SQEle(ConvToBytes(), DefaultCallback);
    enabled = false;
    timer = new Timer(WaitTimeVel);
    cueController = gameObject.transform.Find("CueBall").GetComponent<CueController>();
    ballData = new BallData("init", Vector3.zero);
    rbBalls = gameObject.GetComponentsInChildren<Rigidbody>();
    var tableno_str = gameObject.transform.parent.name.Split('_')[1];
    GameProcess.tables.Add(int.Parse(tableno_str), this);
    UnityEngine.Debug.Log(GameProcess.tables[0]);
  }



  void FixedUpdate()
  {
    netvel = 0.0f;
    foreach (Rigidbody rb in rbBalls)
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
          foreach (Rigidbody rb in rbBalls)//check for null value in rbballs balls are destroyed after pcoketing 
          {
            TableData.Add(new BallData(rb.gameObject.name, rb.position));
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

  private void OnEnable()
  { 

    UnityEngine.Debug.Log(cueController);
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

