﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Text;
// using UnityEngine.JSONSerializeModule;

namespace SerializeData
{
  [Serializable]
  public class BallData
  {
    public String BallName = String.Empty;
    public float x = 0.0f;
    public float z = 0.0f;

    public BallData(String ballname, Vector3 position)
    {
      BallName = ballname;
      x = position.x;
      // y = position.y;
      z = position.z;
    }

    public String serialize()
    {
      return JsonUtility.ToJson(this);
    }
  }

  [Serializable]
  public class SerializableTableData
  {
    [SerializeField]
    public List<BallData> balls = new List<BallData>();
    [SerializeField]
    public int table_no;
    
    public  SerializableTableData(List<BallData> tabledata,int tableno)
    {
      balls = tabledata;
      table_no = tableno;
    }
  }

  [Serializable]
  public class ForceCommand
  {
    public float F = 0.0f;
    public float phsi = 0.0f;
    public float a = 0.0f;
    public float b = 0.0f;
    public int table_id = 0;

    public ForceCommand(float f_, float phsi_, float a_, float b_,int tid)
    {
      F = f_;
      phsi = phsi_;
      a = a_;
      b = b_;
      table_id = tid;
    }

    public static ForceCommand getFc(String jsontext)
    {
      return JsonUtility.FromJson<ForceCommand>(jsontext);
    }

    public Vector3 ConvertToVector()
    {
      return new Vector3(F * Mathf.Cos(phsi), 0.0f, F * Mathf.Sin(phsi));
    }
  }

  [Serializable]
  public class SimGameState
  {
    [SerializeField]
    public List<BallData> balls;
    [SerializeField]
    public ForceCommand force;

    public SimGameState(List<BallData> table_data,ForceCommand fc)
    {
      balls = table_data;
      force =fc;
    }

    public static SimGameState get_SGState(String jsontext)
    {
      return JsonUtility.FromJson<SimGameState>(jsontext);
    }

    public static void jsonprototype()
    {
      BallData ball1 = new BallData("ball1",new Vector3(1.0F,2.0F,3.0F));
      BallData ball2 = new BallData("ball1",new Vector3(4.0F,5.0F,6.0F));
      List<BallData> ballist = new List<BallData>();
      ballist.Add(ball1);
      ballist.Add(ball2);
      ForceCommand f1 = new ForceCommand(1000F,1080F,0.0F,0.0F,1);
      SimGameState sg_state = new SimGameState(ballist,f1);
      Debug.Log(JsonUtility.ToJson(sg_state));
    }
  }

}