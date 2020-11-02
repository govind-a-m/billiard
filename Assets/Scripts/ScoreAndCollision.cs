using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ScoreAndCollision : MonoBehaviour {

    void Start() { }

    void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.CompareTag("Player")) 
        {
            other.transform.position = new Vector3(-23f, 25.95059f, 0f);
            BallController.rb.velocity = Vector3.zero;
            Debug.Log("Player in hole");
        }

        if (other.gameObject.CompareTag("lost")) 
        {
            Debug.Log("lost");
            Destroy(other.gameObject);
        }

        if (other.gameObject.CompareTag("full"))
        { 
			Destroy(other.gameObject);
            BallController.score++;
        }

        if (other.gameObject.CompareTag("half_full")) {
			Destroy(other.gameObject);
            BallController.score++;
        }
    }

    public void returnMenu() {
        Application.LoadLevel("SampleScene");
    }
}
