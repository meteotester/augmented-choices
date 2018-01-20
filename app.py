from flask import Flask,jsonify,json

app = Flask(__name__)

@app.route("/choices")
def getChoices():

    try:

        # Initialize a employee list
        choicesList = []

        # create a instances for filling up employee list
        for i in range(0,2):
            empDict = {
            'name': 'Harry Potter Exhibition',
            'distance': 'Augustine',
            'category': 'Exhibitions',
            'picture': 'http://esphoto360x360.mnstatic.com/781dcbcc32d566bd8762267b9d1435ca'
            }
        choicesList.append(empDict)

        # convert to json data
        jsonStr = json.dumps(choicesList)

    except Exception ,e:
        print str(e)

    return jsonify(jsonStr)

if __name__ == "__main__":
    app.run()
