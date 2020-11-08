using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class GameProcess : MonoBehaviour
{   
    public static ProcessPipeline pipeline;
    public static List<messanger> BallMsgr;

    void Awake()
    {
        pipeline = new ProcessPipeline();
        pipeline.StartPipeLine();
    }

    void Start()
    {   BallMsgr = new List<messanger>();
        foreach (Transform child in gameObject.GetComponentInChildren<Transform>())
        {
            BallMsgr.Add(child.gameObject.GetComponent<messanger>());
        }
    }

    void Update()
    {
        foreach(String msg in pipeline.RecvAll())
        {
            Debug.Log(msg);
        }
    }                    

    private void OnDestroy()
    {
        pipeline.EndSendThread();
    }

}
