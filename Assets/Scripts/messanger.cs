using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SerializeData;
using System;
using SQ;
using System.Text;

public class messanger : MonoBehaviour
{   
    public BallData ball;
    public ProcessPipeline Gp;
    public SQEle MsgTemplate;

    void Start()
    {
        ball = new BallData(gameObject.name,gameObject.transform.position);
        Gp = GameProcess.pipeline;
        MsgTemplate = new SQEle(this.ConvToBytes(),testcallback);
        enabled = false;
    }

    void Update()
    {
        MsgTemplate.data = ConvToBytes();
        Gp.sendQ.Enq(MsgTemplate);
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

    private byte[] ConvToBytes()
    {
        ball.x = gameObject.transform.position.x;
        ball.y = gameObject.transform.position.y;
        ball.z = gameObject.transform.position.z;
        return Encoding.ASCII.GetBytes(ball.serialize()+"END_OF_MSG");
    }
}
