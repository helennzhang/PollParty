
################################################################################
################################################################################
########                                                                ########
########   Python - Firebase - Flask Login/Register App                 ########
########   Author: Hemkesh Agrawal                                      ########
########   Website: http://hemkesh.com                                  ########
########   Last updated on: 11/27/2019                                  ########
########                                                                ########
########   P.S. This is my first ever github project, so I              ########
########   would love to hear your feedback : agrawalh@msu.edu          ########
########                                                                ########
################################################################################
################################################################################

import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_cors import CORS
import requests
import json

app = Flask(__name__)  # Initialze flask constructor

CORS(app)

# Add your own details
config = {
    "apiKey": "AIzaSyBTksv4M7Mdjd8uZ25oF_BGwUn_czGXdwo",
    "authDomain": "technica-75110.firebaseapp.com",
    "databaseURL": "https://technica-75110.firebaseio.com",
    "storageBucket": "technica-75110.appspot.com"
}

# initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

# Login


@app.route("/")
def login():
    return render_template("login.html")

# Sign up/ Register


@app.route("/signup")
def signup():
    return render_template("signup.html")

# Welcome page


@app.route("/welcome")
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email=person["email"], name=person["name"])
    else:
        return redirect(url_for('login'))

# If someone clicks on login, they are redirected to /result


@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        result = request.form  # Get the data
        email = result["email"]
        password = result["pass"]
        try:
            # Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)
            # Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            # Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            # Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            # If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

# If someone clicks on register, they are redirected to /register


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":  # Only listen to POST
        result = request.form  # Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            # Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            # Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            # Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            # Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            # Go to welcome page
            return redirect(url_for('welcome'))
        except:
            # If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route("/welcome/pollsites", methods=["POST"])
def get_pollsites():
    data = request.json
    params = {
        "address": data['address'],
        "electionId": 7000,
        "key": "AIzaSyAEZVE6ADzCTuBKsbHIFt4o12JBZOPA5bE"
    }
    api_url = "https://www.googleapis.com/civicinfo/v2/voterinfo"

    response = requests.get(api_url, params=params)

    return json.loads(response.content.decode('utf-8'))

# get parties and join a party
@app.route("/welcome/joinparty", methods=["POST"])
def joinparty():
    print("here")
    result = request.json  # Get the data submitted
    location = result["locationName"]
    zipcode = result["zip"]
    
    valid_parties = []

    # get parties from db that match location, zip
    try:
        all_parties = db.child("parties").get()
        for party in all_parties.each():
            if party.val()["Location"] == location and party.val()["Zipcode"] == zipcode:
                valid_parties.append({"Location": party.val()["Location"], 
                    "Zipcode": party.val()["Zipcode"], 
                    "people": party.val()["people"]}) #"time": party.val()["time"]

        json_data = json.dumps(valid_parties)

        # send valid parties back 
        return json_data

    except Exception as e:
        print(str(e))
        return str(e) 
        # If there is any error, do nothing

# create a new party
@app.route("/welcome/createparty", methods=["POST"])
def createparty():
    print("here")
    result = request.json  # Get the data submitted
    location = result["locationName"]
    zipcode = result["zip"]
    #time = result["Time"]
    # try to push to db
    try:
        #print("here")
        data = {"Location": location, "Zipcode": zipcode, "people": 1} #, "time": time
        db.child("parties").push(data)
        return "success"

    except:
        return "fail"
        # If there is any error, do nothing


if __name__ == "__main__":
    app.run()
