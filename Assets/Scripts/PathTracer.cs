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
	public List<float> angles;
	public List<float> velocities;
	private Vector2 velvec_xz;
  void Start()
  {
		PathRendr = GetComponent<LineRenderer>();
		rb = GetComponent<Rigidbody>();
		PathPoints = new List<Vector3>();
		angles = new List<float>();
		velocities = new List<float>();
		ballState = BallState.STOPPED; 
		MinMovingVel = MIN_RESTING_VEL+HYST_VEL;
		velvec_xz = new Vector2();
  }

  void FixedUpdate()
  {
		switch(ballState)
		{
			case BallState.STOPPED:
				if(rb.velocity.magnitude>MinMovingVel)
				{	
					PathPoints.Clear();
					angles.Clear();
					velocities.Clear();
					DrawNextPoint(rb.position);
					ballState = BallState.MOVING;
				}
				break;
			case BallState.MOVING:
				DrawNextPoint(rb.position);
				velvec_xz.x = PathPoints[PathPoints.Count-2].x-rb.position.x;
				velvec_xz.y = PathPoints[PathPoints.Count-2].z-rb.position.z;
				angles.Add(Mathf.Deg2Rad*Vector2.Angle(velvec_xz,transform.right));
				velocities.Add(rb.velocity.magnitude);
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
