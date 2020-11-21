using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using SoftwareTimer;
using SQ;
using SerializeData;
using System.Text;

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

  void Start()
  {
    rbBalls = gameObject.GetComponentsInChildren<Rigidbody>();
    TableData = new List<BallData>();
    MsgTemplate = new SQEle(ConvToBytes(), DefaultCallback);
    enabled = false;
    timer = new Timer(WaitTimeVel);
    Gp = GameProcess.pipeline;
    GameProcess.tables.Add(this.TableNo,this);
    cueController = gameObject.transform.Find("CueBall").GetComponent<CueController>();
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
          foreach (Rigidbody rb in rbBalls)
          {
            ballData.BallName = rb.gameObject.name;
            ballData.x = rb.position.x;
            ballData.y = rb.position.y;
            ballData.z = rb.position.z;
            TableData.Add(ballData);
          }
          MsgTemplate.data = ConvToBytes();
          Gp.sendQ.Enq(MsgTemplate);
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
    if(cueController.SimComplete)
    {
      cueController.ApplyForce(Fc);
    }
    else
    {
      UnityEngine.Debug.Log("sim not complete");
    }
  }
  private byte[] ConvToBytes()
  {
    return Encoding.ASCII.GetBytes(JsonUtility.ToJson(TableData) + "END_OF_MSG");
  }

  public void DefaultCallback()
  {

  }

}

