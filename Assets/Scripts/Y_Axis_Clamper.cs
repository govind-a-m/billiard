using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Y_Axis_Clamper : MonoBehaviour
{   
    public Vector3 initialPosition;
    void Start()
    {
        initialPosition = gameObject.transform.position;
    }
    void FixedUpdate()
    {
        if(gameObject.transform.position.y>initialPosition.y)
        {
            gameObject.transform.position = new Vector3(gameObject.transform.position.x,initialPosition.y,gameObject.transform.position.z);
        }        
    }
}
