using System.Collections;
using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.UI;

public class BallController : MonoBehaviour {

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
    public ProcessPipeline pipeline;

    public string ReadData()
    {
        return "test";
    }

    public void HandleReturnMsg(string msg)
    {
        Debug.Log(msg);
    }

    void Start()
    {
        speed = 100;
        maxForce = 5;
        moveVertical = 0;
        playing = true;
        rb = GetComponent<Rigidbody>();
        lineSize = new Vector3(10.0f, 0.0f, 0.0f);
        playerPosition = rb.transform.position;
        endLine = playerPosition + lineSize;
        line = GetComponent<LineRenderer>();
        tm = GameObject.Find("Box001").GetComponent<TableManager>();
        pipeline = new ProcessPipeline() { readData_Func = ReadData, returnData_Func = HandleReturnMsg };
        pipeline.Start();
    }

    void FixedUpdate()
    {
        if (playing) {
            playerPosition = rb.transform.position;

            if (isStrikerOnTable())
            {
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

                if (Input.GetKey(KeyCode.Space))
                {
                    rb.AddForce((endLine - playerPosition) * speed);
                }
                if (Input.GetKey(KeyCode.RightControl))
                {
                    rb.transform.position = new Vector3(-23f, 25.95059f, 0f);
                }
            }
            else
            {
                gameObject.transform.position = new Vector3(-23f, 25.95059f, 0f);
            }
        }
    }

    bool isStrikerOnTable()
    {
        if (rb.velocity.magnitude < ThreshVel)
        { 
            if (tm.ontable.IndexOf("Ball") == -1)
            {
                return false;
            }
}
        return true;
    }


    private void OnDestroy()
    {
        pipeline.Stop();
    }
}
