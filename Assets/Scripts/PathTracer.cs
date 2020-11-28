using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PathTracer : MonoBehaviour
{	
	public LineRenderer PathRendr;
	public Rigidbody rb;
	public List<Vector3> PathPoints;
	public enum BallState
	{
		STOPPED,
		MOVING
	}
	public BallState ballState;
	public float MIN_RESTING_VEL = 0.001f;
	public float HYST_VEL = 0.004f;
	public float MinMovingVel;

  void Start()
  {
		PathRendr = GetComponent<LineRenderer>();
		rb = GetComponent<Rigidbody>();
		PathPoints = new List<Vector3>();
		ballState = BallState.STOPPED; 
		MinMovingVel = MIN_RESTING_VEL+HYST_VEL;
  }

  void FixedUpdate()
  {
		switch(ballState)
		{
			case BallState.STOPPED:
				if(rb.velocity.magnitude>MinMovingVel)
				{	
					PathPoints.Clear();
					Debug.Log(rb.name+" "+rb.velocity.magnitude.ToString());
					DrawNextPoint(rb.position);
					ballState = BallState.MOVING;
				}
				break;
			case BallState.MOVING:
				DrawNextPoint(rb.position);
				if(rb.velocity.magnitude<MIN_RESTING_VEL)
				{
					ballState = BallState.STOPPED;
				}
				break;
		}
  }

	private void DrawNextPoint(Vector3 newP)
	{
		PathPoints.Add(newP);
		PathRendr.positionCount = PathPoints.Count;
		PathRendr.SetPosition(PathPoints.Count-1,newP);
	}

}
