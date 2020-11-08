using System.Collections;
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
}