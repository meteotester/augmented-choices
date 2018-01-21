#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,jsonify,json
from flask import request
import requests
import os
from jsonpath_rw import jsonpath, parse
import sys
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding("utf-8")

app = Flask(__name__)
api_key = os.environ['API_KEY_MINUBE']

subcategories = json.load(open('data/subcategories.json'))

subcategories_dict = {x["id"]:x["name"] for x in subcategories}

def selectFields(mydict):
    import unidecode

    mydict["subcategory"] = subcategories_dict[mydict["subcategory_id"]]
    mydict["name"] = unidecode.unidecode(mydict["name"])

    mydict = {k:mydict[k] for k in ('id', 'name','distance', 'subcategory', 'picture_url') if k in mydict}
    return mydict



@app.route('/choices')
def getChoices():
    if (int(request.args['profile']) > 0):
        choicesList = [{'name': 'children', 'text': 'Cosas de chavales'}, {'name':'family', 'text': 'Para toda la familia'}]
    else:
        choicesList = [{'name': 'nightlife', 'text': 'Ajetreo hasta el amanecer'}, {'name':'symbols', 'text': 'Simbolos de la ciudad'}]
    print choicesList
    jsonStr = json.dumps(choicesList)
    result = '{"Choices":'+json.dumps(choicesList)+'}'

    print result
    return result


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

    return jsonStr

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

    return jsonStr


@app.route('/hotels')
def getHotels():
    # At the moment profile is not taken into account and criteria is hardcoded
    # Moreover we are connecting to the sandbox

    from json import load
    from urllib2 import urlopen

    myip = load(urlopen('http://jsonip.com'))['ip']

    #import socket
    #myip = socket.gethostbyname(socket.gethostname())
    print myip

    url = "https://sandbox.hotelscombined.com/api/2.0/hotels/basic?destination=place:Vigo&checkin=2018-03-28&checkout=2018-03-31&rooms=2&apiKey=%s&sessionID=null&onlyIfComplete=False&languageCode=ES&starRating=5&clientIp=%s" %(os.environ['API_KEY_HOTELSCOMBINED'], myip)
    print url

    headers = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

    r = requests.get(url, headers=headers)

    # Return top 2 choices
    myjson = r.json()
    myjson["results"] = myjson["results"][0:2]

    jsonStr = json.dumps(myjson)
    return jsonStr


if __name__ == "__main__":
    app.run(host='0.0.0.0')
