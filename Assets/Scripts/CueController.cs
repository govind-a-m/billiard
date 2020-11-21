using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SerializeData;

public class CueController : MonoBehaviour
{	
	public Rigidbody cue;
  public bool _SimComplete {get;}
	public float MAX_RestingVel = 0.01f;
	public float BallRadius;

	void Awake()
  {
		cue = GetComponent<Rigidbody>();
		BallRadius = GetComponent<SphereCollider>().radius;
  }

	public bool SimComplete
	{
		get
		{
			if(cue.velocity.magnitude>MAX_RestingVel)
			{
				return false;
			}
			else
			{
				return true;
			}
		}
	}

	public void ApplyForce(ForceCommand fc)
	{
		cue.velocity = Vector3.zero;
		cue.rotation = Quaternion.identity;
		Vector3 force_vec = fc.ConvertToVector();
		Vector3 impact_loc = new Vector3(cue.position.x + BallRadius * Mathf.Cos(fc.phsi),
																		 cue.position.y,
																		 cue.position.z + BallRadius * Mathf.Sin(fc.phsi));
		cue.AddForceAtPosition(force_vec, impact_loc, ForceMode.Impulse);
	}


}
