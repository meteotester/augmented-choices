using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class fadeOutScript : MonoBehaviour {
	public GameObject letterImage;
	// Use this for initialization
	void Start () {
		StartCoroutine(eraseLetter());
	}
	
	// Update is called once per frame
	void Update () {
		
	}
	IEnumerator eraseLetter(){
		yield return new WaitForSeconds(6f);
		//iTween.ScaleTo(letterImage, new Vector3(0f, 0f, 0f ), 1f);
		letterImage.SetActive (false);
		yield break;
	}
}
