#!/usr/bin/python
# -*- coding: latin-1 -*-
from flask import Flask,jsonify,json
from flask import request
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



@app.route('/choices')
def getChoices():
    if (int(request.args['profile']) > 0):
        choicesList = [{'name': 'children', 'text': 'Cosas de niños'}, {'name':'family', 'text': 'Para toda la familia'}]
    else:
        choicesList = [{'name': 'nightlife', 'text': 'Ajetreo hasta el amanecer'}, {'name':'symbols', 'text': 'Símbolos de la ciudad'}]
    print choicesList
    jsonStr = json.dumps(choicesList)
    return jsonify(jsonStr)


@app.route("/experience")
def getExperience():

    try:
        lat=40.465511
        lng=-3.618767
        choice='symbols'
        if (request.args['lat']):
            lat = request.args['lat']
        if (request.args['lng']):
            lng = request.args['lng']
        if (request.args['choice']):
            choice = request.args['choice']
        experiencesList = []
        url ="http://papi.minube.com/pois?lang=en&latitude=%s&longitude=%s&max_distance=500&order_by=distance&api_key=%s" %(lat,lng,api_key)
        print url
        r = requests.get(url)

        # fill choices list
        for i in range(0,1):
            empDict = selectFields(r.json()[i])
            experiencesList.append(empDict)

        print experiencesList
        # convert to json data
        jsonStr = json.dumps(experiencesList[0])

    except Exception ,e:
        print str(e)

    return jsonify(jsonStr)

if __name__ == "__main__":
    app.run()
