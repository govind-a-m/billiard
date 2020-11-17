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
    public float y = 0.0f;
    public float z = 0.0f;
    
    public BallData(String ballname,Vector3 position)
    {
      BallName = ballname;
      x = position.x;
      y = position.y;
      z = position.z;
    }

    public String serialize()
    {
      return JsonUtility.ToJson(this);
    }
  }


  [Serializable]
  public class ForceCommand
  {
    public float F = 0.0f;
    public float phsi = 0.0f;
    public float a = 0.0f;
    public float b = 0.0f;
  
    public ForceCommand(float f_,float phsi_,float a_,float b_)
    {
      F = f_;
      phsi = phsi_;
      a = a_;
      b = b_;
    }

    public static ForceCommand getFc(String jsontext)
    {
      return JsonUtility.FromJson<ForceCommand>(jsontext);
    }

    public Vector3 ConvertToVector()
    {
      return new Vector3(F*Mathf.Cos(phsi),0.0f,F*Mathf.Sin(phsi));
    }

    
  }
}