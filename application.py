from flask import Flask, flash, redirect, render_template, request, session
from flask.ext.session import Session
import sqlite3
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from decimal import Decimal
from helpers import apology, login_required

# Configure application
app = Flask(__name__)
companyid = "";
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

@app.route("/registerCompany", methods=["GET", "POST"])
def registerCompany():
    """Register company"""

    if request.method == "POST":

        print(companyid)

        # check/store company name
        if not request.form.get("companyname"):
            return apology("Missing company name.")
        companyname = request.form.get("companyname")
        print(companyname)

        # check/store company phone number
        if not request.form.get("phone"):
            return apology("Missing company phone number.")
        phone = request.form.get("phone")

        # check/store owner first name
        if not request.form.get("firstname"):
            return apology("Missing first name.")
        firstname = request.form.get("firstname")

        # check/store owner last name
        if not request.form.get("lastname"):
            return apology("Missing last name.")
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
        
        db.execute("""SELECT companyname FROM companies
                      WHERE companyname = ?;""", (companyname,))
        rows = db.fetchall()
        if len(rows) > 0:
            return apology("Company name exists. Re-enter correct incorporation number.")

        # insert new owner into database
        result = db.execute("""INSERT INTO owners (firstname, lastname, email, hash) 
                               VALUES (?,?,?,?);""", (firstname, lastname, email, hash))


# TODO: retrieve companyid on form submit from scripts.js

        # insert new company into database
        db.execute("""INSERT INTO companies (companyid, companyname, phone) 
                      VALUES (?,?,?);""", (companyid, companyname, phone))

        # user must provide unique email address 
        if not result:
            return apology("Email address already in use.")

        conn.commit()
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

        # check for email
        if not request.form.get("email"):
            return apology("Missing email address.")

        # check for password
        elif not request.form.get("password"):
            return apology("Enter a password.")

        # check for password confirmation
        elif not request.form.get("confirmation"):
            return apology("Confirm password.")

        # check for matching passwords
#        elif not request.form.get("cell"):
#            return apology("Enter driver cell number")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.")

        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        hash = generate_password_hash(request.form.get("password"))
   
# TODO: CHECK TO ENSURE OWNER WANTS THIS USER UNDER HIS TEAM?
#       CONSIDER STORING companyid IN GLOBAL VARIABLE

        # insert new user into database
        result = db.execute("""INSERT INTO operators (firstname, lastname, email, hash) 
                              VALUES (?,?,?,?);""", (firstname, lastname, email, hash))

# TODO: CONSIDER SELECTING FROM ANOTHER TABLE 'TRUCKS' WHERE EACH TRUCK
# TODO: IS REGISTERED TO ITS OWNER AND COMPANY? ENSURE THE OWNER HAS A
# TODO: TRUCK ASSIGNED TO THIS OPERATOR?

        # user must provide unique email address 
        if not result:
            return apology("Email address already in use.")

        conn.commit()
        # successful registration redirect
        return render_template("login.html")


    # registration redirect
    else:
        return render_template("registeroperator.html")


@app.route("/getCompanyName", methods=["GET","POST"])
def getCompanyName():
    """return company name from code"""

    companyname = ""
    global companyid
    if request.method == "POST":

        # check for company code
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



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("missing email address", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("missing password", 403)

        email = request.form.get("email")

        # Query database for email address
        db.execute("""SELECT * FROM operators 
                      WHERE email = ?;""", (email,))

        rows = db.fetchall()
        print(rows)
        print(rows[0])
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Change user password"""

    if request.method =="POST":
        # check form filled
        if not request.form.get("oldpassword"):
            return apology("Enter old password")

        elif not request.form.get("newpassword"):
            return apology("Enter new password")

        elif not request.form.get("confirmation"):
            return apology("Confirm new password")

        # check for matching new password
        elif request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        # query for current password hash
        oldhash = db.execute("SELECT hash FROM users WHERE id=:id", \
                              id=session["user_id"])

        # check current password validity
        if not check_password_hash(oldhash[0]["hash"], request.form.get("oldpassword")):
            return apology("Re-enter current password")

        # hash and update new password
        db.execute("UPDATE users SET hash=:hash WHERE id=:id", \
                    hash=generate_password_hash(request.form.get("newpassword")), \
                    id=session["user_id"])

        return redirect("/")

    else:
        return render_template("settings.html")



@app.route("/")
@login_required
def index():
    """Logged in screen"""
#
#    # populate user portfolio
#    wallet = db.execute("SELECT shares, symbol FROM portfolio \
#                         WHERE id=:id", id=session["user_id"])
#    balance = 0
#
#    # iterate through user-owned stocks
#    for stock in wallet:
#        symbol = stock["symbol"]
#        shares = stock["shares"]
#        stockinfo = lookup(symbol)
#        total = int(shares) * float(stockinfo["price"])
#
#        balance += total
#
#        # update user portfolio
#        db.execute("UPDATE portfolio SET price=:price, \
#                    total=:total WHERE id=:user_id AND symbol=:symbol", \
#                    price=usd(stockinfo["price"]), total=usd(total), \
#                    user_id=session["user_id"], symbol=symbol)
#
#    # load user cash balance from users database
#    cash = db.execute("SELECT cash FROM users WHERE id=:user_id", \
#                        user_id=session["user_id"])
#
#    # update balance
#    balance += cash[0]["cash"]
#
#    # query database for user portfolio
#    portfolio = db.execute("SELECT * FROM portfolio WHERE id=:user_id", \
#                            user_id=session["user_id"])
#
#    return render_template("index.html", portfolio=portfolio, \
#                            cash=usd(cash[0]["cash"]), \
#                            total=usd(balance))
#
#
    return render_template("index.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)



# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
