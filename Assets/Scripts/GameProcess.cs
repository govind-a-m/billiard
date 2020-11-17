using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using SerializeData;


public class GameProcess : MonoBehaviour
{   
    public static ProcessPipeline pipeline;
    public static List<messanger> BallMsgr;
    public static Rigidbody striker_rb;
    public static ForceCommand Fc;
    private static int _NofRecvdMsgs {get;}

    void Awake()
    {   
        BallMsgr = new List<messanger>();
        pipeline = new ProcessPipeline();
        pipeline.StartPipeLine();
        foreach (Transform child in gameObject.GetComponentInChildren<Transform>())
        {
            BallMsgr.Add(child.gameObject.GetComponent<messanger>());
            if(child.gameObject.name=="CueBall")
            {
                striker_rb = child.gameObject.GetComponent<Rigidbody>();
            }
        }
        Fc = new ForceCommand(0.0f,0.0f,0.0f,0.0f);
    }

    void Update()
    {
        foreach(String msg in pipeline.RecvAll())
        {
            Debug.Log(msg);
            Fc = ForceCommand.getFc(msg);
        }
    }                    

    public static void DisableMessangers()
    {   
        foreach(messanger msgr in BallMsgr)
        {
            if(msgr!=null) // when ball gets pocketed this will be null
            {
                msgr.DisableMessanger();
            }
        }
    }

    public static void EnableMessangers(messanger.BROADCAST_MODE bcst_mode)
    {   
        foreach(messanger msgr in BallMsgr)
        {
            if(msgr!=null)
            {
                msgr.EnableMessanger(bcst_mode);
            }
        }
    }

    public static bool StrikerMoving()
    {
        if(striker_rb.velocity.magnitude>0.01)
        {
            return true;
        }
        return false;
    }

    private void OnDestroy()
    {
        pipeline.EndSendThread();
    }

    public static int NofRecvdMsgs
    {
        get {return pipeline.recvQ.Q.Count;}
    }
}
