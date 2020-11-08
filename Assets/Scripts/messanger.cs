using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SerializeData;
using System;
using SQ;
using System.Text;
using SoftwareTimer;

public class messanger : MonoBehaviour
{   
    public BallData ball;
    public ProcessPipeline Gp;
    public SQEle MsgTemplate;
    public Rigidbody rb;
    public float VelocityThreshold = 0.05f;
    public float WaitTimeVel = 0.1f;
    public float BroadcastPeriod = 0.1f;
    public Timer timer;
    public Timer BroadcastTimer;

    void Start()
    {
        ball = new BallData(gameObject.name,gameObject.transform.position);
        Gp = GameProcess.pipeline;
        MsgTemplate = new SQEle(this.ConvToBytes(),DefaultCallback);
        rb = GetComponent<Rigidbody>();
        enabled = false;
        timer = new Timer(WaitTimeVel);
        BroadcastTimer = new Timer(BroadcastPeriod); 
        
    }

    void FixedUpdate()
    {   if(BroadcastTimer.Expired(Time.deltaTime))
        {   BroadcastTimer.ResetTimer();
            if((rb.velocity.magnitude>VelocityThreshold) || (GameProcess.StrikerMoving()))
            {
                MsgTemplate.data = ConvToBytes();
                Gp.sendQ.Enq(MsgTemplate);
                timer.ResetTimer();
            }
            else
            {   
                if(timer.status=="STARTED")
                {
                    if(timer.Expired(Time.deltaTime))
                    {   
                        enabled = false;
                        timer.ResetTimer();
                    }
                }
                else{
                    timer.Start();
                }
            }
        }
        else
        {
            timer.value += Time.deltaTime;
        }
    }

    public void EnableMessanger()
    {
        enabled = true;
    }

    public void DisableMessanger()
    {
        enabled = false;
    }

    public void testcallback()
    {
        Debug.Log(ball.BallName);
    }

    public void DefaultCallback()
    {
        
    }

    private byte[] ConvToBytes()
    {
        ball.x = gameObject.transform.position.x;
        ball.y = gameObject.transform.position.y;
        ball.z = gameObject.transform.position.z;
        return Encoding.ASCII.GetBytes(ball.serialize()+"END_OF_MSG");
    }
}
