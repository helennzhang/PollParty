
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
    print(data)
    params = {
        "address": data['address'],
        "electionId": 7000,
        "key": "AIzaSyAEZVE6ADzCTuBKsbHIFt4o12JBZOPA5bE"
    }
    api_url = "https://www.googleapis.com/civicinfo/v2/voterinfo"

    response = requests.get(api_url, params=params)

    return response.text


if __name__ == "__main__":
    app.run()
