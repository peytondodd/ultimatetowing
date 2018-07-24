def teamManagement():
    """Owner team management page"""
    

    companyid = session["companyid"] 

    # query for operators in company
    db.execute("""SELECT * FROM operators 
                    WHERE companyid=?""", 
            (companyid, ))
    team = db.fetchall()

    # pass team to jinja in html
    return render_template("teammanagement.html", team=team)

def removeOperator():
    """Owner removes operator from team"""

    if not request.args.get("operatorid"):
        raise RuntimeError("Error: something went wrong!")

    operatorid = request.args.get("operatorid")

    # query for operator details
    db.execute("""SELECT 
                    date_registered,
                    operatorid,
                    firstname,
                    lastname,
                    email,
                    hash,
                    cell,
                    companyid 
                  FROM operators
                  WHERE operatorid=?;""", (operatorid, ))
    operator = db.fetchall()[0]

    # add operator into archived_operators table
    db.execute("""INSERT INTO archived_operators (
                    date_archived,
                    date_registered,
                    operatorid,
                    firstname,
                    lastname,
                    email,
                    hash,
                    cell,
                    companyid )
                  VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?);""", (
                    operator[0],
                    operator[1],
                    operator[2],
                    operator[3],
                    operator[4],
                    operator[5],
                    operator[6],
                    operator[7], ))
    conn.commit()
        
    # delete operator from operators
    db.execute("""DELETE FROM operators
                  WHERE operatorid = ?;""", 
                  (operatorid, )) 
    conn.commit()

    # reload team management page
    return teamManagement() 

def truckManagement():
    """Owner truck management page"""

    companyid = session["companyid"] 

    # query for company trucks
    db.execute("""SELECT * FROM trucks WHERE companyid=?""", 
                  (companyid, ))
    garage = db.fetchall()

    # pass garage to jinja in html
    return render_template("truckmanagement.html", garage=garage)

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
        
        db.execute("""INSERT INTO trucks (
                        make, 
                        model, 
                        licenseplate, 
                        companyid )
                      VALUES (?,?,?,?);""", (
                        make, 
                        model, 
                        licenseplate, 
                        companyid, ))
        conn.commit()

        # redirect user to pound management
        return redirect("/truckManagement")

    else:
        # redirect to form
        return render_template("addtruck.html")

def removeTruck():
    """Owner removes truck from company"""

    if not request.args.get("truckid"):
        raise RuntimeError("Error: something went wrong!")

    truckid = request.args.get("truckid")

    # query for operator details
    db.execute("""SELECT 
                    truckid,
                    make,
                    model,
                    licenseplate,
                    companyid,
                    operatorid
                  FROM trucks
                  WHERE truckid=?;""", (truckid, ))
    truck = db.fetchall()[0]

    # add operator into archived_trucks table
    db.execute("""INSERT INTO archived_trucks (
                    truckid,
                    make,
                    model,
                    licenseplate,
                    companyid,
                    operatorid )
                  VALUES (?,?,?,?,?,?);""", (
                    truck[0],
                    truck[1],
                    truck[2],
                    truck[3],
                    truck[4],
                    truck[5], ))
    conn.commit()
        
    # delete operator from operators
    db.execute("""DELETE FROM trucks
                  WHERE truckid = ?;""", (truckid, )) 
    conn.commit()

    # reload team management page
    return truckManagement() 

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

    #TODO: Geocode address and store long, lat

        db.execute("""INSERT INTO pounds (
                        address, 
                        city, 
                        phone, 
                        companyid )
                      VALUES (?,?,?,?);""", (
                        address, 
                        city, 
                        phone, 
                        companyid, ))
        conn.commit()

        # redirect user to pound management
        return redirect("/poundManagement")

    else:
        # redirect to form
        return render_template("addpound.html")

def removePound():
    """Owner removes pound from company"""

    if not request.args.get("poundid"):
        raise RuntimeError("Error: something went wrong!")

    poundid = request.args.get("poundid")

    # query for operator details
    db.execute("""SELECT 
                    poundid,
                    address,
                    city,
                    phone,
                    companyid
                  FROM pounds
                  WHERE poundid=?;""", (poundid, ))
    pound = db.fetchall()[0]

    archived_date = datetime.datetime.now()

    # add pound into archived_pounds table
    db.execute("""INSERT INTO archived_pounds (
                    poundid,
                    address,
                    city,
                    phone,
                    companyid )
                  VALUES (?,?,?,?,?);""", (
                    pound[0],
                    pound[1],
                    pound[2],
                    pound[3],
                    pound[4], ))
    conn.commit()
        
    # delete operator from operators
    db.execute("""DELETE FROM pounds
                  WHERE poundid = ?;""", 
                  (poundid, )) 
    conn.commit()

    # reload pound management page
    return poundManagement() 
