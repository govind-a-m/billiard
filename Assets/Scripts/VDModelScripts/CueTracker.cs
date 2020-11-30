using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class CueTracker : MonoBehaviour
{
	public Vector3 ForceVec;
	public Camera cam;
	public float MinMovingVelocity = 0.001f;
	public Rigidbody rb;
	public String BallState = "STOPPED";
	public float displacement = 0.0f;
	public Vector3 InitLoc;
	private int stop_count = 0;
  void Awake()
  {
		rb = GetComponent<Rigidbody>();
		ForceVec = new Vector3(0.0f,0.0f,0.0f);
  }

  // void FixedUpdate()
  // {
	// 	if(rb.velocity.magnitude<MinMovingVelocity)
	// 	{
	// 		BallState = "STOPPED";
	// 		displacement = Vector3.Distance(rb.position,Vector3.zero);
	// 	}
	// }

	public void ApplyForce(float fvel)
	{	
		rb.position = InitLoc;
		BallState = "MOVING";
		ForceVec.z = fvel;
		stop_count = 0;
		rb.AddForce(ForceVec,ForceMode.VelocityChange);
	}

	public bool isStopped()
	{
		if(rb.velocity.magnitude<MinMovingVelocity)
		{	
			if(stop_count>2)
			{	
				BallState = "STOPPED";
				displacement = Vector3.Distance(rb.position,InitLoc);
				return true;
			}
			stop_count++;
		}
		return false;
	}
}

