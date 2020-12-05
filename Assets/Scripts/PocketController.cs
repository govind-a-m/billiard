using UnityEngine;
using System.Collections;

public class PocketController : MonoBehaviour 
{
	public GameObject Balls;
	public GameObject cueBall;

	private Vector3 originalCueBallPosition;

	void Start() 
	{
		originalCueBallPosition = cueBall.transform.position;
	}

	void OnCollisionEnter(Collision collision) 
	{
		foreach (var transform in Balls.GetComponentsInChildren<Transform>()) 
		{
			if (transform.name == collision.gameObject.name) 
			{	
				if (cueBall.transform.name == collision.gameObject.name) 
				{
					cueBall.transform.position = originalCueBallPosition;
				}
				else
				{
					collision.gameObject.SetActive(false);
				}
			}
		}
	}
}
