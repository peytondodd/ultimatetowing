def incidentReport():
    """Incident Report Form"""
    # create new incident report

    if request.method =="POST":

        # check/store customer information
        if not request.form.get("name"):
            return apology("Enter customer name")
        elif not request.form.get("address"):
            return apology("Enter customer address")
        elif not request.form.get("phone"):
            return apology("Enter customer phone number")
        elif not request.form.get("insurancecompany"):
            return apology("Enter customer insurance company")
        elif not request.form.get("insurancepolicy"):
            return apology("Enter customer insurance policy number")

        # input from customer information
        name = request.form.get("name")
        address = request.form.get("address")
        phone = request.form.get("phone")
        insurancecompany = request.form.get("insurancecompany")
        insurancepolicy = request.form.get("insurancepolicy")

        # add to table: customers
        db.execute("""INSERT INTO customers (
                        name,
                        address,
                        phone,
                        insurancecompany,
                        insurancepolicy )
                      VALUES (?,?,?,?,?);""", (
                        name,
                        address,
                        phone,
                        insurancecompany,
                        insurancepolicy, ))

        # check/store customer vehicle details
        if not request.form.get("year"):
            return apology("Enter vehicle year")
        elif not request.form.get("make"):
            return apology("Enter vehicle make")
        elif not request.form.get("model"):
            return apology("Enter vehicle model")
        elif not request.form.get("mileage"):
            return apology("Enter vehicle mileage")
        elif not request.form.get("color"):
            return apology("Enter vehicle color")
        elif not request.form.get("licenseplate"):
            return apology("Enter vehicle license plate")
        elif not request.form.get("vin"):
            return apology("Enter vehicle VIN") 
        
        # input from customer vehicle details
        year = request.form.get("year")
        make = request.form.get("make")
        model = request.form.get("model")
        mileage = request.form.get("mileage")
        color = request.form.get("color")
        licenseplate = request.form.get("licenseplate")
        vin = request.form.get("vin")
        operatorid = session["user_id"]

        # add to table: cust_vehicles
        db.execute("""INSERT INTO cust_vehicles (
                        year,
                        make,
                        model,
                        mileage,
                        color,
                        licenseplate,
                        vin,
                        operatorid )
                      VALUES (?,?,?,?,?,?,?,?);""", (
                        year,
                        make,
                        model,
                        mileage,
                        color,
                        licenseplate,
                        vin,
                        operatorid, ))

        # check/store incident details
        if not request.form.get("pickup"):
            return apology("Enter incident location")
        elif not request.form.get("dropoff"):
            return apology("Enter drop-off location")
        #elif not request.form.get("crcused"):
        #    return apology("TODO: DEAL WITH NO CRC")
        

        # input from incident details
        pickup = request.form.get("pickup")
        dropoff = request.form.get("dropoff")
        crcused = request.form.get("crcused")
        flattire = request.form.get("flattire")
        flatbed = request.form.get("flatbed")
        dollies = request.form.get("dollies")
        boost = request.form.get("boost")
        fuel = request.form.get("fuel")
        winch = request.form.get("winch")
        lockout = request.form.get("lockout")
        collision = request.form.get("collision")
        towed = request.form.get("towed")
        keys = request.form.get("keys")
        poundid = request.form.get("poundid")
        companyid = session["companyid"] 

        db.execute("""SELECT vehicleid 
                        FROM cust_vehicles
                       WHERE vin=?;""", (vin, ))
        vehicleid = db.fetchall()[0][0]

        # add to table: incidents
        db.execute("""INSERT INTO incidents (
                        incidentdate,
                        pickup,
                        dropoff,
                        crcused,
                        flattire,
                        flatbed,
                        dollies,
                        boost,
                        fuel,
                        winch,
                        lockout,
                        collision,
                        towed,
                        keys,
                        companyid,
                        operatorid,
                        vehicleid,
                        poundid )
                      VALUES (CURRENT_TIMESTAMP,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", (
                        pickup,
                        dropoff,
                        crcused,
                        flattire,
                        flatbed,
                        dollies,
                        boost,
                        fuel,
                        winch,
                        lockout,
                        collision,
                        towed,
                        keys,
                        companyid,
                        operatorid,
                        vehicleid,
                        poundid, ))

        # add to table: impounded_vehicles
        db.execute("""INSERT INTO impounded_vehicles (
                        impounded_date,
                        vehicleid,
                        poundid,
                        operatorid )
                      VALUES (CURRENT_TIMESTAMP,?,?,?);""", (
                        vehicleid,
                        poundid,
                        operatorid, ))
        conn.commit()

        return redirect("/incidentHistory")

    return render_template("incidentreport.html")

def incidentHistory():
    """Operator incident history"""
    operatorid = session["user_id"] 

    # query for company trucks
    db.execute("""SELECT * FROM incidents WHERE operatorid=?""", 
                  (operatorid, ))
    history = db.fetchall()

    # pass list of incidents to jinja in html
    return render_template("incidenthistory.html", history=history)

def impoundedVehicles():
    """Operator's list of impounded vehicles"""
    operatorid = session["user_id"] 
    
    db.execute("""SELECT 
                    status, 
                    poundid, 
                    round(julianday('now') - julianday(impounded_date), 0),
                    cust_vehicles.year, 
                    cust_vehicles.make, 
                    cust_vehicles.model 
                  FROM impounded_vehicles 
                  INNER JOIN cust_vehicles 
                  ON cust_vehicles.vehicleid = impounded_vehicles.vehicleid 
                  WHERE cust_vehicles.operatorid = ?;""", 
                  (operatorid, ))

    # query for impounded vehicles by operatorid
    impounded_vehicles = db.fetchall()
    print(impounded_vehicles)

    # pass list of incidents to jinja in html
    return render_template("impoundedvehicles.html", impounded_vehicles=impounded_vehicles)

