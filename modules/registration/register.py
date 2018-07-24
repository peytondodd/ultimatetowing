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

def linkOwnerCompany(ownerid, companyid):
    """Create link between company and owner in owners_companies"""
    
    # add link in joint table for owner & company
    db.execute("""INSERT INTO owners_companies 
                      VALUES (?, ?);""", 
                      (ownerid, companyid))
    
    conn.commit()
    

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

