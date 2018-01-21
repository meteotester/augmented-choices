using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class controlsScript : MonoBehaviour {

	private float moneyStatus = 1f;
	public GameObject buttonLow;
	public GameObject buttonMed;
	public GameObject buttonHigh;

	public Text adultosText;
	public Text ninosText;
	public Text bebesText;

	public CanvasGroup mainCanvas;
	public CanvasGroup selectPlaceCanvas;

	public Text choice1Text;
	public Text choice2Text;

	private float adultos = 0f;
	private float ninos = 0f;
	private float bebes = 0f;

	// Use this for initialization
	void Start () {
		PlayerPrefs.SetString ("family", "0");
	}
	
	// Update is called once per frame
	void Update () {
		
	}
	public void changeMoneyStatus(float newStatus){
		moneyStatus = newStatus;
		if (newStatus == 1f) {
			buttonLow.SetActive (false);
			buttonMed.SetActive (true);
			buttonHigh.SetActive (true);
		}
		if (newStatus == 2f) {
			buttonLow.SetActive (true);
			buttonMed.SetActive (false);
			buttonHigh.SetActive (true);
		}
		if (newStatus == 3f) {
			buttonLow.SetActive (true);
			buttonMed.SetActive (true);
			buttonHigh.SetActive (false);
		}
	}
	public void changeAdultStatics(float cant){
		adultos += cant;
		if (adultos < 0f)
			adultos = 0f;
		adultosText.text = adultos.ToString();
		if (adultos + ninos + bebes == 0f)
			PlayerPrefs.SetString ("family", "0");
		else
			PlayerPrefs.SetString ("family", "1");
	}
	public void changeNinosStatics(float cant){
		ninos += cant;
		if (ninos < 0f)
			ninos = 0f;
		ninosText.text = ninos.ToString();
		if (adultos + ninos + bebes == 0f)
			PlayerPrefs.SetString ("family", "0");
		else
			PlayerPrefs.SetString ("family", "1");
	}
	public void changeBebesStatics(float cant){
		bebes += cant;
		if (bebes < 0f)
			bebes = 0f;
		bebesText.text = bebes.ToString();
		if (adultos + ninos + bebes == 0f)
			PlayerPrefs.SetString ("family", "0");
		else
			PlayerPrefs.SetString ("family", "1");
	}
	public void fadeMainMenu(){
		StartCoroutine("FadeOutMain");
	}
	public void fadeselectPlaceMenu(){
		StartCoroutine("selectPlaceFadeOut");
		StartCoroutine (changeChoices());
	}
	IEnumerator FadeOutMain(){
		float time = 1f;
		while(mainCanvas.alpha > 0){
			mainCanvas.alpha -= 2*(Time.deltaTime / time);
			if (mainCanvas.alpha == 0)
				mainCanvas.gameObject.SetActive (false);
			yield return null;
		}
	}
	IEnumerator selectPlaceFadeOut(){
		float time = 1f;
		while(selectPlaceCanvas.alpha > 0){
			selectPlaceCanvas.alpha -= 2*(Time.deltaTime / time);
			if (selectPlaceCanvas.alpha == 0)
				selectPlaceCanvas.gameObject.SetActive (false);
			yield return null;
		}
	}
	IEnumerator changeChoices() {
		while (true) {
			string familyOption = PlayerPrefs.GetString ("family");
			Debug.Log (familyOption);

			//string weatherUrl = "http://api.openweathermap.org/data/2.5/weather?q=Madrid,ES&units=metric&appid=ab68bc64552d2af53af0f6b928972688";
			//string weatherUrl = "http://192.168.0.161:5000/choices?profile=0";
			string weatherUrl = string.Concat("http://129.158.75.253:5000/choices?profile=", familyOption);
			WWW weatherWWW = new WWW (weatherUrl);

			yield return weatherWWW;

			JSONObject tempData = new JSONObject (weatherWWW.text);

			Debug.Log (tempData);

			string text1 = tempData["Choices"][1]["text"].str;
			string text2 = tempData["Choices"][0]["text"].str;

			choice1Text.text = text1;
			choice2Text.text = text2;

			PlayerPrefs.SetString ("opcion1", tempData["Choices"][1]["name"].str );
			PlayerPrefs.SetString ("opcion2", tempData["Choices"][0]["name"].str );

			yield return new WaitForSeconds(60);
		}
	}
}
