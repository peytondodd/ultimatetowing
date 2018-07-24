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
        db.execute("""SELECT companyname 
                        FROM companies
                       WHERE companyname = ?;""", (companyname,))

        rows = db.fetchall()
        if len(rows) > 0:
            return apology("Company name exists. Re-enter correct incorporation number.")

        # insert new owner into database
        result = db.execute("""INSERT INTO owners (
                                firstname, 
                                lastname, 
                                email, 
                                hash, 
                                date_registered ) 
                               VALUES (?,?,?,?,CURRENT_TIMESTAMP);""", 
                               (firstname, lastname, email, hash))

        # insert new company into database
        db.execute("""INSERT INTO companies (
                        companyid, 
                        companyname, 
                        phone ) 
                      VALUES (?,?,?);""", 
                      (companyid, companyname, phone))

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

