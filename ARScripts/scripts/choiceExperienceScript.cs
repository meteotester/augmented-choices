using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class choiceExperienceScript : MonoBehaviour {

	private int sceneNumber;
	// Use this for initialization
	void Start () {
	}
	void Update () {
		
	}
	public void startExperienceButton(int opc){
		if( opc == 1 )StartCoroutine (startExperience(PlayerPrefs.GetString ("opcion1")));
		if( opc == 2 )StartCoroutine (startExperience(PlayerPrefs.GetString ("opcion2")));
		sceneNumber = opc;
	}
	IEnumerator startExperience(string optionSelected) {
		while (true) {
			Debug.Log (optionSelected);
			string weatherUrl = string.Concat("http://129.158.75.253:5000/experience?lat=40.469943&lng=-3.616984&choice=", optionSelected);
			WWW weatherWWW = new WWW (weatherUrl);

			yield return weatherWWW;

			JSONObject tempData = new JSONObject (weatherWWW.text);

			Debug.Log (tempData);
			string weatherMain = tempData["distance"].str;
			SceneManager.LoadScene (sceneNumber);
			yield return new WaitForSeconds(60);
		}
	}
}
