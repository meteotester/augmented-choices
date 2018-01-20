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
    mydict = {k:mydict[k] for k in ('id', 'name','distance', 'subcategory', 'picture_url') if k in mydict}
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


@app.route("/placetoeat")
def getPlacetoeat():

    try:
        lat=40.465511
        lng=-3.618767
        if (request.args['lat']):
            lat = request.args['lat']
        if (request.args['lng']):
            lng = request.args['lng']

        myfilter = "&category_group=eat"
        experiencesList = []
        url ="http://papi.minube.com/pois?lang=es&city_id=1252&latitude=%s&longitude=%s&order_by=score&max_distance=1000&api_key=%s%s" %(lat,lng,api_key,myfilter)
        print url
        r = requests.get(url)

        if (len(r.json()) == 0):
            url ="http://papi.minube.com/pois?lang=es&city_id=1252&latitude=%s&longitude=%s&order_by=score&api_key=%s%s" %(lat,lng,api_key,myfilter)
            print url
            r = requests.get(url)

        myjson = r.json()

        # Len 5 fixes bug with id 0
        for i in range(min(5,len(myjson))):
            empDict = selectFields(myjson[i])

            # Exclude blacklist
            if (empDict["id"]) not in [0]:
                experiencesList.append(empDict)

        print(experiencesList)

        # convert to json data
        jsonStr = json.dumps(experiencesList[0])

    except Exception ,e:
        print str(e)

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

        subcategory = ""
        if choice == "symbols":
            #Statues
            subcategory = "&subcategory_id=16"
        if choice == "family":
            #Exhibitions
            subcategory = "&subcategory_id=82"
        if choice == "nightlife":
            #Nightclubs
            subcategory = "&subcategory_id=39"
        if choice == "children":
            #Sports-Related
            subcategory = "&subcategory_id=87"


        experiencesList = []
        url ="http://papi.minube.com/pois?lang=es&city_id=1252&latitude=%s&longitude=%s&order_by=score&max_distance=1000&api_key=%s%s" %(lat,lng,api_key,subcategory)
        print url
        r = requests.get(url)
        if (len(r.json()) == 0):
            url ="http://papi.minube.com/pois?lang=es&city_id=1252&latitude=%s&longitude=%s&order_by=score&api_key=%s%s" %(lat,lng,api_key,subcategory)
            print url
            r = requests.get(url)

        myjson = r.json()
        # fill choices list
        for i in range(len(myjson)):
            empDict = selectFields(myjson[i])
            if (empDict["id"]) not in ["25128", "3707046", "2198"]:
                experiencesList.append(empDict)

        print(experiencesList)

        # convert to json data
        jsonStr = json.dumps(experiencesList[0])

    except Exception ,e:
        print str(e)

    return jsonify(jsonStr)

if __name__ == "__main__":
    app.run()
