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
            db.execute("""SELECT hash 
                            FROM owners 
                           WHERE ownerid = ?;""", \
                          (session["user_id"],))
            rows = db.fetchall()
        elif session["user_type"] == "Operator":
            db.execute("""SELECT hash 
                            FROM operators 
                           WHERE operatorid = ?;""", \
                          (session["user_id"],))
            rows = db.fetchall()

        oldhash = rows[0][0]

        # check current password validity
        if not check_password_hash(oldhash, request.form.get("oldpassword")):
            return apology("Re-enter current password")

        # check for the use
        # hash and update new password
        if session["user_type"] == "Owner":
            db.execute("""UPDATE owners 
                            SET hash = ? 
                            WHERE ownerid = ?""", \
                            (generate_password_hash(request.form.get("newpassword")), 
                            session["user_id"]))

        elif session["user_type"] == "Operator":
            db.execute("""UPDATE operators 
                            SET hash = ? 
                            WHERE operatorid = ?""", \
                            (generate_password_hash(request.form.get("newpassword")), 
                            session["user_id"]))

        # save changes to the database
        conn.commit()

        # password change success, send home
        return redirect("/")

    else:
        # password change failed, refresh settings
        return render_template("settings.html")
