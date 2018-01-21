using UnityEngine;
using System.Collections;

public class rotateObject : MonoBehaviour {

	// Use this for initialization

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		transform.Rotate(Vector3.right * Time.deltaTime * (4f));
	}
}
