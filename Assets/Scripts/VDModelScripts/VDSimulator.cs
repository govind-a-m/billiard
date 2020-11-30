using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;


[Serializable]
public class VDdata
{
	[SerializeField]
	public float v;
	[SerializeField]
	public float d;

	public VDdata(float v_,float d_)
	{
		v = v_;
		d = d_;
	}
}

[Serializable]
public class VDSimResult
{
	[SerializeField]
	public List<VDdata> results = new List<VDdata>();
	
	public VDSimResult(List<VDdata> sim_results)
	{
		results = sim_results;
	}
}

public class VDSimulator : MonoBehaviour
{
  public GameObject CuePrefab;
	public int MaxNofBalls = 100;
	public float step_x = 2.0f;
	private GameObject cueinstance;
	public List<CueTracker> cues;
	public float V_min = 5.0f;
	public float V_max = 50.0f;
	public float V_Current = 5.0f;//same as v min
	public float V_step = 5.0f;
	public int NofActive = 0;
	public Vector3 SpawnLoc = new Vector3(0.0f,0.5f,0.0f);
	public Dictionary<float,float> SimResult = new Dictionary<float, float>();

	void Awake()
  {	
		Spawnat(0.0f);
		for(int i=2;i<MaxNofBalls/2;i++)
		{	
			Spawnat(i*step_x);
			Spawnat(-i*step_x);
		}
  }

	private void Spawnat(float x)
	{
		SpawnLoc.x = x;
		cueinstance = Instantiate(CuePrefab,SpawnLoc,Quaternion.identity);
		cues.Add(cueinstance.GetComponent<CueTracker>());
		cues[cues.Count-1].InitLoc = SpawnLoc;
	}

	void Start()
	{
		foreach(var cue in cues)
		{
			if(V_Current<V_max)
			{
				cue.ApplyForce(V_Current);
				SimResult.Add(V_Current,0.0f);
				V_Current += V_step;
			}
			else
			{
				break;
			}
		}
	}

  void FixedUpdate()
  {	
		NofActive = cues.Count;
		foreach(var cue in cues)
		{	
			if(cue.isStopped())
			{	
				//Debug.Log(cue.ForceVec.ToString()+" "+cue.displacement.ToString());
				SimResult[cue.ForceVec.z] = cue.displacement;
				NofActive = NofActive-1;
				if(V_Current<V_max)
				{
					cue.ApplyForce(V_Current);
					SimResult.Add(V_Current,0.0f);
					V_Current += V_step;
					NofActive++;
				}
			}
		}
		//Debug.Log("Nof active:"+NofActive.ToString());
		if((NofActive<=0) & (V_Current>=V_max))
		{	
			Debug.Log("done with simulation");
			List<VDdata> ListSimResult = new List<VDdata>();
			foreach(var key in SimResult.Keys)
			{
				ListSimResult.Add(new VDdata(key,SimResult[key]));
			}
			String jsontext = JsonUtility.ToJson(new VDSimResult(ListSimResult)); // shivane shambulingaaaa!!!
			Debug.Log(jsontext);
			System.IO.File.WriteAllText(@"VDSimResult.txt", jsontext);
			enabled = false;
		}
	}
}

