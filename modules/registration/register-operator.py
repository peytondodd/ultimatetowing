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
        result = db.execute("""INSERT INTO operators  (
                                 firstname, 
                                 lastname, 
                                 email, 
                                 hash, 
                                 member, 
                                 date_registered, 
                                 companyid ) 
                               VALUES (?,?,?,?,?,CURRENT_TIMESTAMP,?);""",
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
