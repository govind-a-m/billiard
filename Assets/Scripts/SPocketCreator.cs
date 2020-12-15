using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SPocketCreator : MonoBehaviour
{	
	public GameObject SPock;
  void Awake()
  {
		var go = Instantiate(SPock,gameObject.transform);
    go.SetActive(true);
  }
}
