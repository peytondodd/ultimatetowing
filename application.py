from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask.ext.session import Session
import sqlite3
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from decimal import Decimal
from helpers import apology, login_required

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

@app.route("/getCompanyName", methods=["GET","POST"])
def getCompanyName():
    """return company name from code"""

    companyname = ""
    if request.method == "POST":

        # check/store company code
        if not request.form.get("companyid"):
            return apology("must provide company code", 403)
        companyid = request.form.get("companyid") 

        # query database for company code
        db.execute("""SELECT companyname FROM companies 
                      WHERE companyid = ?;""", (companyid,))
        
        rows = db.fetchall()
        if len(rows) > 0:
            companyname = rows[0]

    return companyname


@app.route("/requestOwnership", methods=["GET", "POST"])
def requestOwnership():
    """Request being added as company owner"""

    if request.method == "POST":
        
        # check/store company id
        if not request.form.get("companyid"):
            return apology("Missing company id.")
        companyid = request.form.get("companyid")
        
        # check/store owner name
        if not request.form.get("firstname"):
            return apology("Missing first name.")
        if not request.form.get("lastname"):
            return apology("Missing last name.")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        
        # check/store owner email
        if not request.form.get("email"):
            return apology("Missing email address.")
        email = request.form.get("email")

        # check/store owner password
        if not request.form.get("password"):
            return apology("Enter a password.")
        elif not request.form.get("confirmation"):
            return apology("Confirm password.")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")
        hash = generate_password_hash(request.form.get("password"))

        # check/store owner cell
        if not request.form.get("cell"):
            return apology("Missing cell address.")
        cell = request.form.get("cell")

        # insert new owner into database
        result = db.execute("""INSERT INTO owners (firstname, lastname, 
                               email, hash, cell) VALUES (?,?,?,?,?);""",
                               (firstname, lastname, email, hash, cell))

        # user must provide unique email address 
        if not result:
            return apology("Email address already in use.")

        # query for current owner
        db.execute("""SELECT owners.ownerid FROM owners INNER JOIN owners_companies 
                      ON owners_companies.ownerid = owners.ownerid WHERE 
                      owners_companies.companyid = ?;""", (companyid, ))

        rows = db.fetchall() 
        ownerid = rows[0][0]
        # TODO: send request to current owner with new ownerid

        conn.commit()

        # successful registration direct
        return render_template("login.html")

    # request ownership redirect
    else:
        return render_template("requestownership.html")

@app.route("/registerCompany", methods=["GET", "POST"])
def registerCompany():
    """Register company"""

    if request.method == "POST":

        # check/store company id
        if not request.form.get("companyid"):
            return apology("Missing company id.")
        companyid = request.form.get("companyid")

        # check/store company name
        if not request.form.get("companyname"):
            return apology("Missing company name.")
        companyname = request.form.get("companyname")

        # check/store company phone number
        if not request.form.get("phone"):
            return apology("Missing company phone number.")
        phone = request.form.get("phone")

        # check/store owner name
        if not request.form.get("firstname"):
            return apology("Missing first name.")
        if not request.form.get("lastname"):
            return apology("Missing last name.")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")

        # check/store owner email
        if not request.form.get("email"):
            return apology("Missing email address.")
        email = request.form.get("email")

        # check/store owner password
        if not request.form.get("password"):
            return apology("Enter a password.")
        elif not request.form.get("confirmation"):
            return apology("Confirm password.")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")
        hash = generate_password_hash(request.form.get("password"))
        
        # query database for company
        db.execute("""SELECT companyname FROM companies
                      WHERE companyname = ?;""", (companyname,))

        rows = db.fetchall()
        if len(rows) > 0:
            return apology("Company name exists. Re-enter correct incorporation number.")

        # insert new owner into database
        result = db.execute("""INSERT INTO owners (firstname, lastname, email, hash) 
                               VALUES (?,?,?,?);""", (firstname, lastname, email, hash))

        # insert new company into database
        db.execute("""INSERT INTO companies (companyid, companyname, phone) 
                      VALUES (?,?,?);""", (companyid, companyname, phone))

        # user must provide unique email address 
        if not result:
            return apology("Email address already in use.")

        # get newly registered owner's id
        db.execute("""SELECT ownerid FROM owners WHERE email = ?;""", (email, ))
        rows = db.fetchall()
        ownerid = rows[0][0]

        conn.commit()

        # call link function
        linkOwnerCompany(ownerid, companyid)

        # successful registration redirect
        return render_template("login.html")

    # registration redirect
    else:
        return render_template("registercompany.html")


@app.route("/registerOperator", methods=["GET", "POST"])
def registerOperator():
    """Register operator"""

    if request.method == "POST":

        # check for name
        if not request.form.get("firstname"):
            return apology("Missing first name.")
        if not request.form.get("lastname"):
            return apology("Missing last name.")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        
        # check for email
        if not request.form.get("email"):
            return apology("Missing email address.")
        email = request.form.get("email")

        # check/store owner password
        if not request.form.get("password"):
            return apology("Enter a password.")
        elif not request.form.get("confirmation"):
            return apology("Confirm password.")
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")
        hash = generate_password_hash(request.form.get("password"))

        # check for company id
        if not request.form.get("companyid"):
            return apology("Missing company id")
        companyid = request.form.get("companyid")

        # insert new user into database
        result = db.execute("""INSERT INTO operators (firstname, lastname, 
                               email, hash, member, companyid) VALUES (?,?,?,?,?,?);""",
                               (firstname, lastname, email, hash, 0, companyid))

        # user must provide unique email address 
        if not result:
            return apology("Email address already in use.")

        conn.commit()
        # successful registration redirect
        return render_template("login.html")


    # registration redirect
    else:
        return render_template("registeroperator.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Form submission check 
        if not request.form.get("email"):
            return apology("missing email address", 403)
        elif not request.form.get("password"):
            return apology("missing password", 403)
        elif not request.form.get("usertype"):
           return apology("user? owner? wat ru bruv?")
        email = request.form.get("email")
        usertype = request.form.get("usertype")

        rows = None
        # Query database for email address
        if usertype == "Operator":
            db.execute("""SELECT operatorid, email, hash FROM operators
                          WHERE email = ?;""", (email,))
            rows = db.fetchall()

        elif usertype == "Owner":
            db.execute("""SELECT ownerid, email, hash FROM owners 
                          WHERE email = ?;""", (email,))
            rows = db.fetchall()

        # Ensure username exists and password is correct
        if len(rows) !=1:
            return apology("Email not recognized", 403)
        if not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("Incorrect password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0][0]
        session["user_type"] = usertype

        # store companyid
        db.execute("""SELECT companyid FROM owners_companies 
                      WHERE ownerid=?;""", (session["user_id"], ))
        rows = db.fetchall() 
        session["companyid"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/searchCompany")
def searchCompany():
    """Search for companies that match query"""

    # check for query
    if not request.args.get("q"):
        raise RuntimeError("Search failed")

    # add wildcard to query and search database
    q = "%" + request.args.get("q") + "%"
    db.execute("""SELECT * FROM companies WHERE companyid LIKE ? 
                  OR companyname LIKE ? LIMIT 5;""", (q,q))
    
    rows = db.fetchall()
    
    return jsonify(rows)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change user password"""
    
    oldhash = None
    rows = None

    if request.method =="POST":
        # ensure form completion
        if not request.form.get("oldpassword"):
            return apology("Enter old password")
        elif not request.form.get("newpassword"):
            return apology("Enter new password")
        elif not request.form.get("confirmation"):
            return apology("Confirm new password")

        # check for matching new password
        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("New passwords do not match")

        # query for hash of password
        if session["user_type"] == "Owner":
            db.execute("""SELECT hash FROM owners WHERE ownerid = ?;""", \
                          (session["user_id"],))
            rows = db.fetchall()
        elif session["user_type"] == "Operator":
            db.execute("""SELECT hash FROM operators WHERE operatorid = ?;""", \
                          (session["user_id"],))
            rows = db.fetchall()

        oldhash = rows[0][0]

        # check current password validity
        if not check_password_hash(oldhash, request.form.get("oldpassword")):
            return apology("Re-enter current password")

        # check for the use
        # hash and update new password
        if session["user_type"] == "Owner":
            db.execute("""UPDATE owners SET hash = ? WHERE ownerid = ?""", \
                          (generate_password_hash(request.form.get("newpassword")), session["user_id"]))

        elif session["user_type"] == "Operator":
            db.execute("""UPDATE operators SET hash = ? WHERE operatorid = ?""", \
                          (generate_password_hash(request.form.get("newpassword")), session["user_id"]))

        # save changes to the database
        conn.commit()

        # password change success, send home
        return redirect("/")

    else:
        # password change failed, refresh settings
        return render_template("settings.html")



@app.route("/")
@login_required
def index():
    """Logged in screen"""
    # display relevant dashboard (owner/operator)

    if session["user_type"] == "Owner":

        return redirect("/teamManagement")

    elif session["user_type"] == "Operator":
        return redirect("/incidentReport")


####################################################################
########################## Owner Functions #########################
####################################################################

@app.route("/teamManagement")
@login_required
def teamManagement():
    """Owner team management page"""

    companyid = session["companyid"] 

    # query for operators in company
    db.execute("""SELECT * FROM operators WHERE companyid=?""", 
            (companyid, ))
    team = db.fetchall()

    # pass team to jinja in html
    return render_template("teammanagement.html", team=team)


@app.route("/truckManagement")
@login_required
def truckManagement():
    """Owner team management page"""
    # display relevant dashboard (owner/operator)

    companyid = session["companyid"] 

    # query for company trucks
    db.execute("""SELECT * FROM trucks WHERE companyid=?""", 
                  (companyid, ))
    garage = db.fetchall()

    # pass garage to jinja in html
    return render_template("truckmanagement.html", garage=garage)


@app.route("/poundManagement")
@login_required
def poundManagement():
    """Owner team management page"""
    # display pound information

    companyid = session["companyid"] 

    # query for pounds
    db.execute("""SELECT * FROM pounds WHERE companyid=?""", 
                  (companyid, ))
    pounds = db.fetchall()

    # pass pounds to jinja in html
    return render_template("poundmanagement.html", pounds=pounds)


####################################################################
######################## Operator Functions ########################
####################################################################

@app.route("/incidentReport")
@login_required
def incidentReport():
    """Owner team management page"""
    # display relevant dashboard (owner/operator)

    return render_template("incidentreport.html")

@app.route("/incidentHistory")
@login_required
def incidentHistory():
    """Owner team management page"""
    # display relevant dashboard (owner/operator)

    return render_template("incidenthistory.html")

@app.route("/impoundedVehicles")
@login_required
def impoundedVehicles():
    """Owner team management page"""
    # display relevant dashboard (owner/operator)

    return render_template("impoundedvehicles.html")


##############################################################
######################## Map Function ########################
##############################################################

@app.route("/map")
@login_required
def map():
    """Owner team management page"""
    # display relevant dashboard (owner/operator)

    return render_template("map.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/addPound", methods=["GET", "POST"])
@login_required
def addPound():
    """Add new pound to company"""

    if request.method == "POST":

        # check/store pound address
        if not request.form.get("address"):
            return apology("Missing address.")
        address = request.form.get("address")

        # check/store pound city
        if not request.form.get("city"):
            return apology("Missing city.")
        city = request.form.get("city")

        # check/store pound phone number
        if not request.form.get("phone"):
            return apology("Missing company phone number.")
        phone = request.form.get("phone")
        
        companyid = session["companyid"]

    #TODO: Geocode address and store long, lat? or consider calling function to retrieve geocode?

        db.execute("""INSERT INTO pounds (address, city, phone, companyid)
                      VALUES (?,?,?,?);""", (address, city, phone, companyid, ))
        conn.commit()

        # redirect user to pound management
        return redirect("/poundManagement")

    else:
        # redirect to form
        return render_template("addpound.html")



@app.route("/addTruck", methods=["GET", "POST"])
@login_required
def addTruck():
    """Add truck to company fleet"""

    if request.method == "POST":

        # check/store truck make
        if not request.form.get("make"):
            return apology("Missing make.")
        make = request.form.get("make")

        # check/store truck model
        if not request.form.get("model"):
            return apology("Missing model.")
        model = request.form.get("model")

        # check/store truck license plate
        if not request.form.get("licenseplate"):
            return apology("Missing license plate number.")
        licenseplate = request.form.get("licenseplate")
        
        companyid = session["companyid"]

    #TODO: assign operator to truck (currently nullable in db)
        #operatorid = session["operatorid"]
        
        db.execute("""INSERT INTO trucks (make, model, licenseplate, companyid)
                      VALUES (?,?,?,?);""", (make, model, licenseplate, companyid, ))
        conn.commit()

        # redirect user to pound management
        return redirect("/truckManagement")

    else:
        # redirect to form
        return render_template("addtruck.html")

        

def linkOwnerCompany(ownerid, companyid):
    """Create link between company and owner in owners_companies"""
    
    # add link in joint table for owner & company
    db.execute("""INSERT INTO owners_companies 
                      VALUES (?, ?);""", (ownerid, companyid))
    
    conn.commit()
    

def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)



# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
