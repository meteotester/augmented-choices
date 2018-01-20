from flask import Flask,jsonify,json
import requests
import os
from jsonpath_rw import jsonpath, parse

app = Flask(__name__)
api_key = os.environ['API_KEY_MINUBE']

subcategories = json.load(open('data/subcategories.json'))
subcategories_dict = {x["id"]:x["name"] for x in subcategories}

def selectFields(mydict):
    mydict["subcategory"] = subcategories_dict[mydict["subcategory_id"]]
    mydict = {k:mydict[k] for k in ('name','distance', 'subcategory', 'picture_url') if k in mydict}
    return mydict


@app.route("/choices")
def getChoices(lat=40.465511, lng=-3.618767):

    try:
        # Initialize a employee list
        choicesList = []

        r = requests.get('http://papi.minube.com/pois?lang=en&latitude=%s&longitude=%s&max_distance=500&order_by=distance&api_key=%s'%(lat,lng,api_key))

        # fill choices list
        for i in range(0,2):
            empDict = selectFields(r.json()[i])
            choicesList.append(empDict)

        # convert to json data
        jsonStr = json.dumps(choicesList)

    except Exception ,e:
        print str(e)

    return jsonify(jsonStr)

if __name__ == "__main__":
    app.run()
