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
            db.execute("""SELECT operatorid, email, hash 
                            FROM operators
                           WHERE email = ?;""", (email,))
            rows = db.fetchall()

        elif usertype == "Owner":
            db.execute("""SELECT ownerid, email, hash 
                            FROM owners 
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

        if usertype == "Owner":
            # store companyid
            db.execute("""SELECT companyid 
                            FROM owners_companies 
                           WHERE ownerid=?;""", (session["user_id"], ))
            rows = db.fetchall() 
            session["companyid"] = rows[0][0]

        elif usertype == "Operator":
            # store companyid
            db.execute("""SELECT companyid 
                            FROM operators 
                           WHERE operatorid=?;""", (session["user_id"], ))
            rows = db.fetchall() 
            session["companyid"] = rows[0][0]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")

