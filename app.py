from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.ext.session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from decimal import Decimal
from helpers import apology, login_required

from account-utils import settings
from dashboard-utils import mapset, operator, owner
from login import login
from registration import register-company, register-operator, register

import sqlite3
import datetime

# Configure application
app = Flask(__name__)
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure SQLite database
conn = sqlite3.connect("towing.db", check_same_thread=False)
db = conn.cursor()

@app.route("/")
@login_required
def index():
    """Logged in screen"""
    # display relevant dashboard (owner/operator)

    if session["user_type"] == "Owner":

        return redirect("/teamManagement")

    elif session["user_type"] == "Operator":
        return redirect("/incidentReport")


@app.route("/getCompanyName", methods=["GET","POST"])
getCompanyName()

@app.route("/requestOwnership", methods=["GET", "POST"])
requestOwnership()

@app.route("/registerCompany", methods=["GET", "POST"])
registerCompany()

@app.route("/registerOperator", methods=["GET", "POST"])
registerOperator()

@app.route("/login", methods=["GET", "POST"])
login()

@app.route("/searchCompany")
searchCompany()

@app.route("/settings", methods=["GET", "POST"])
@login_required
settings()

###################
# Owner Functions #
###################

@app.route("/teamManagement")
@login_required
teamManagement()

@app.route("/removeOperator", methods=["GET", "POST"])
removeOperator()

@app.route("/truckManagement")
@login_required
truckManagement()

@app.route("/addTruck", methods=["GET", "POST"])
@login_required
addTruck()

@app.route("/removeTruck", methods=["GET", "POST"])
removeTruck()

@app.route("/poundManagement")
@login_required
poundManagement()

@app.route("/addPound", methods=["GET", "POST"])
@login_required
addPound()

@app.route("/removePound", methods=["GET", "POST"])
removePound()


######################
# Operator Functions #
######################

@app.route("/incidentReport", methods=["GET", "POST"])
@login_required
incidentReport()

@app.route("/incidentHistory")
@login_required
incidentHistory()


@app.route("/impoundedVehicles")
@login_required
impoundedVehicles()


#################
# Map Functions #
#################

@app.route("/map")
@login_required
def map():
    return render_template("map.html")

@app.route("/updateCoordinates")
updateCoordinates()

@app.route("/logout")
logout()

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
