using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

namespace  SoftwareTimer
{
    public class Timer 
    {   
        public String status = String.Empty;
        public float value;
        public float limit;

        public Timer(float max_val)
        {
            status = "INIT";
            value = 0.0f;
            limit = max_val;
        }

        public bool Expired(float delta_time)
        {   value = value+delta_time;
            if(value>=limit)
            {   
                status = "EXPIRED";
                return true;
            }
            return false;
        }

        public void Start()
        {
            status = "STARTED";
            value = 0.0f;
        }

        public void ResetTimer()
        {
            value = 0.0f;
            status = "INIT";
        }
    }
}