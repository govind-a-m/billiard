#if false
using System.Collections;
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.UI;
using SQ;
using System.Text;
using System;

public class BallController : MonoBehaviour
{

  public static int score = 0;
  public float ThreshVel = 0.001f;
  public static Rigidbody rb;
  public static bool playing;
  public float moveVertical;
  public float speed;
  public Vector3 playerPosition;
  public Vector3 endLine;
  public Vector3 lineSize;
  public LineRenderer line;
  public int maxForce;
  public Rigidbody striker;
  private TableManager tm;
  public float BallRadius;

  public enum RUN_MODES
  {
    HUMAN,
    PSA
  }
  public RUN_MODES run_mode;
  void Start()
  {
    speed = 100;
    maxForce = 5;
    moveVertical = 0;
    playing = true;
    rb = GetComponent<Rigidbody>();
    lineSize = new Vector3(6.0f, 0.0f, 0.0f);
    playerPosition = rb.transform.position;
    endLine = playerPosition + lineSize;
    line = GetComponent<LineRenderer>();
    BallRadius = GetComponent<SphereCollider>().radius;
    // tm = GameObject.Find("Box001").GetComponent<TableManager>();
  }


  public void FixedUpdate()
  {
    if (run_mode == RUN_MODES.HUMAN)
    {
      ProcessHumanInps();
    }
    else
    {
      ProcessPSAInps();
    }
  }

  public void ProcessHumanInps()
  {
    playerPosition = rb.transform.position;
    if (Input.GetKey(KeyCode.LeftArrow))
    {
      Quaternion rotate = Quaternion.Euler(0, -2, 0);
      lineSize = rotate * lineSize;
    }
    if (Input.GetKey(KeyCode.RightArrow))
    {
      Quaternion rotate = Quaternion.Euler(0, 2, 0);
      lineSize = rotate * lineSize;
    }
    endLine = playerPosition + lineSize;
    moveVertical += Input.GetAxis("Vertical");
    if (moveVertical >= maxForce)
    {
      moveVertical = maxForce;
    }
    endLine += lineSize.normalized * moveVertical;
    line.SetPosition(0, playerPosition);
    line.SetPosition(1, endLine);
    if (rb.velocity.magnitude < ThreshVel)
    {
      if (Input.GetKey(KeyCode.Space))
      {
        Vector3 force_mode_force = (endLine - playerPosition) * speed;
        force_mode_force.y = 0.0f;
        rb.AddForce(force_mode_force, ForceMode.Acceleration);
      }
    }
  }

  public void ProcessPSAInps()
  {
    if (rb.velocity.magnitude < ThreshVel)
    {
      if (GameProcess.Fc.F > 0.0f)
      {
        Debug.Log("recived command" + GameProcess.Fc.ToString());
        rb.velocity = Vector3.zero;
        // bring ball back to ground?
        rb.rotation = Quaternion.identity;
        Vector3 force_vec = GameProcess.Fc.ConvertToVector();
        Vector3 impact_loc = new Vector3(gameObject.transform.position.x - BallRadius * Mathf.Cos(GameProcess.Fc.phsi),
                                        gameObject.transform.position.y,
                                        gameObject.transform.position.z - BallRadius * Mathf.Sin(GameProcess.Fc.phsi));
        rb.AddForceAtPosition(force_vec, impact_loc, ForceMode.VelocityChange);
      }
    }
  }

  public void tempsendcallback()
  {
    Debug.Log("temp callback");
  }
}

// public bool isStrikerOutOfTable()
// {
//     if (rb.velocity.magnitude < ThreshVel)
//     { 
//         if (tm.ontable.IndexOf("Ball") == -1)
//         {
//             return true;
//         }
//     }
//     return false;
// }
#endif