using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class GameProcess : MonoBehaviour
{   
    public static ProcessPipeline pipeline;
    public static List<messanger> BallMsgr;
    public static Rigidbody striker_rb;

    void Awake()
    {   
        BallMsgr = new List<messanger>();
        pipeline = new ProcessPipeline();
        pipeline.StartPipeLine();
        foreach (Transform child in gameObject.GetComponentInChildren<Transform>())
        {
            BallMsgr.Add(child.gameObject.GetComponent<messanger>());
            if(child.gameObject.name=="white")
            {
                striker_rb = child.gameObject.GetComponent<Rigidbody>();
            }
        }
    }

    void Update()
    {
        foreach(String msg in pipeline.RecvAll())
        {
            Debug.Log(msg);
        }
    }                    

    public static void DisableMessangers()
    {   
        foreach(messanger msgr in BallMsgr)
        {
            msgr.DisableMessanger();
        }
    }

    public static void EnableMessangers()
    {   
        foreach(messanger msgr in BallMsgr)
        {
            msgr.EnableMessanger();
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

}
