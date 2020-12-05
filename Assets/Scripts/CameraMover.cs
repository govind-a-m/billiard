using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Text;
using System;

public class CameraMover : MonoBehaviour
{	
	public static Dictionary<String,Vector3> tables = new Dictionary<string, Vector3>();
	private Transform child;
	public Vector3 BirdEyeLocation;
	public static float CameraHeightFromTable = 75;
	public String SelectedTable;
	public enum View
	{
		CAMERA_LOCAL,
		CAMERA_GLOBAL
	}
	public View camera_view = View.CAMERA_GLOBAL;
	private Vector3 HeightVec = new Vector3(0.0f,CameraHeightFromTable,0.0f);

	void Start()
  {
		BirdEyeLocation = gameObject.transform.position;
		foreach(Transform child in transform.parent.transform)// script is attached to camera 
		{
			if(child.gameObject.CompareTag("Table"))
			{
				tables.Add(child.gameObject.name,Camera.main.WorldToScreenPoint(child.gameObject.transform.position));
			}
		}
  }

  void Update()
  {	
		switch(camera_view)
		{	
			case View.CAMERA_LOCAL:
				if(Input.GetKeyDown("space"))
				{
					gameObject.transform.position = BirdEyeLocation;
					camera_view = View.CAMERA_GLOBAL;
				}
				break;
			case View.CAMERA_GLOBAL:
				if(Input.GetKeyDown("space"))
				{
					float min_dst_table = 100000f;
					foreach(var tablename in tables.Keys)
					{
						if(Vector3.Distance(Input.mousePosition,tables[tablename])<min_dst_table)
						{
							min_dst_table = Vector3.Distance(Input.mousePosition,tables[tablename]);
							SelectedTable = tablename;
						}
					}
					gameObject.transform.position = GameObject.Find(SelectedTable).transform.position+HeightVec;
					camera_view = View.CAMERA_LOCAL;
				}
				break;
		}
  }

}
