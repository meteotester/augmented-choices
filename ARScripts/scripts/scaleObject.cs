using UnityEngine;
using System.Collections;

public class scaleObject : MonoBehaviour {
	public GameObject ObjectToScale;
	public Vector3 scaleBefore;
	public float rotateCoef;
	public float timeInit;
	public float TimeDuration;
	public float GeneralPLay;
	public iTween.EaseType easeType;

	// Use this for initialization
	void Start () {
		StartCoroutine(changePositionr(scaleBefore));
	}
	
	// Update is called once per frame
	void Update () {
		transform.Rotate(Vector3.right * Time.deltaTime * (rotateCoef));
	}

	IEnumerator changePositionr(Vector3 pos){

	 	yield return new WaitForSeconds(timeInit + GeneralPLay);
		iTween.ScaleTo ( ObjectToScale, iTween.Hash(
	    		"x"    , pos.x,
	    		"y"    , pos.y,
	    		"z"    , pos.z,
	    		"easeType", easeType,
	    		"time" , TimeDuration,
	    		"delay" , 0f
	 		));
		yield return new WaitForSeconds(3f);
		/*iTween.ScaleTo ( ObjectToScale, iTween.Hash(
	    		"x"    , 0,
	    		"y"    , 0,
	    		"z"    , 0,
	    		"easeType", easeType,
	    		"time" , TimeDuration,
	    		"delay" , 0f
	 		));*/
	    yield break;
	}
}
