def updateCoordinates():
    """Update truck coordinates in database"""

    lat = request.args.get("lat")
    lng = request.args.get("lng")

    print("New coordinates")
    print("Latitude: " + lat)
    print("Longitude: " + lng)

    if session["user_type"] == "Operator":
        # for testing purposes, we'll record all position changes
        db.execute("""INSERT OR REPLACE
                      INTO active_trucks (
                        lat, lng, operatorid ) 
                        VALUES (?,?,?);""", \
                        (lat,lng,session["user_id"],))
        conn.commit()

    return "True" 



@app.route("/update")
update()

def update():
    """get active truck coordinates"""
    
    trucks = []

    # get position of active trucks
    db.execute("""SELECT operatorid, lat, lon 
                    FROM active_trucks 
                    WHERE operatorid = ?;""", \
                    (session["user_id"],))

    rows = db.fetchall()

    for row in rows:

        truck = {
                "operatorid": row[0],
                "lat": row[1],
                "lon": row[2]
        }
        
        trucks.append(truck.copy())

    return trucks

