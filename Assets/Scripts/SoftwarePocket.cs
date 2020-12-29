using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SoftwarePocket : MonoBehaviour
{	
	public  Vector3 originalCueBallPosition;
	public  GameObject cueball;
	void Start()
	{
		cueball = gameObject.transform.parent.transform.parent.Find("Balls/CueBall").gameObject;
		originalCueBallPosition = cueball.transform.position;
	}

	void OnTriggerEnter(Collider other)
	{
		if(other.gameObject.name=="CueBall")
		{
			cueball.transform.position = originalCueBallPosition;
			Rigidbody rb = cueball.gameObject.GetComponent<Rigidbody>(); 
			rb.velocity = Vector3.zero;
			rb.angularVelocity = Vector3.zero;
			rb.rotation = Quaternion.identity;
		}
		else
		{	
			Rigidbody rb = other.gameObject.GetComponent<Rigidbody>(); 
			rb.velocity = Vector3.zero;
			rb.angularVelocity = Vector3.zero;
			rb.rotation = Quaternion.identity;
			other.gameObject.SetActive(false);
		}
	}
}
