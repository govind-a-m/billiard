using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

public class TableManager : MonoBehaviour
{
    public List<string> ontable = new List<string>();
    private Transform[] ts;
    void Start()
    {   ts = GameObject.Find("Balls").GetComponentsInChildren<Transform>();
        foreach (Transform child in ts)
        {
            ontable.Add(child.gameObject.name);
        }
    }

    void OnCollisionEnter(Collision other)
    {
        if(ontable.IndexOf(other.gameObject.name) == -1)
        {
            ontable.Add(other.gameObject.name);
        }
    }

    void OnCollisionExit(Collision other)
    {
        ontable.Remove(other.gameObject.name);
    }


}
