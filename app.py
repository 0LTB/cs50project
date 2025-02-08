from flask import Flask, render_template, request, redirect, session, url_for
from helpers import db_conn, str_generator as str_gen


app = Flask(__name__)
app.config["DEBUG"] = True

app.secret_key = "SECRECY_IS_THE_KEY"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Get list of pubs from database
        pubs_list = db_conn.execute_query("SELECT * FROM pubs ORDER BY name;", fetchall=True)
        error_message = request.args.get('error')
        
        # Check if session has poll_id
        if "poll_id" not in session:
            # Generate string for session's unique URL
            session["poll_id"] = str_gen.create_sequence()
            seq = session["poll_id"]
            return render_template("index.html", pubs_list=pubs_list, seq=seq)
        return render_template("index.html", pubs_list=pubs_list, seq=session["poll_id"], error=error_message)

    if request.method == "POST":
        # Redirect to create new poll and clear session
        if "new_poll" in request.form:
            session.pop("poll_id", None)
            session.pop("voted", None)
            return redirect(url_for("index"))
        
        if "add_pub" in request.form:
            return redirect(url_for("add"))

        # Check if user has voted      
        voted = request.form.get("preference")
        if not voted:
            error = "Please select a pub."
            return redirect(url_for("index", error=error, seq=session["poll_id"]))
        
        # Insert vote into database
        db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES  (%s, %s, %s);", (session["poll_id"], voted, 1))
        session["voted"] = True
        return redirect(url_for("result", seq=session["poll_id"]))
    

@app.route("/result/<seq>", methods=["GET", "POST"])
def result(seq):
    # List of pubs with total votes
    if request.method == "GET":
        error_message = request.args.get('error')
        
        pubs_list = db_conn.execute_query("SELECT pubs.id,\
                                        pubs.name,\
                                        pubs.address,\
                                        pubs.web,\
                                        COALESCE(polls.sum, 0) AS total_votes,\
                                        polls.id,\
                                        pubs.picture\
                                        FROM (\
                                          SELECT polls.id, \
                                          pubs_id, SUM(polls.vote) AS sum\
                                          FROM polls\
                                          WHERE polls.id = %s\
                                          GROUP BY polls.id, pubs_id\
                                        ) polls\
                                        RIGHT JOIN pubs ON pubs.id = polls.pubs_id\
                                        ORDER BY total_votes DESC, pubs.name;", (seq, ), fetchall=True)

        return render_template("result.html", pubs_list=pubs_list, seq=seq, error=error_message)

    # Insert vote into database
    if request.method == "POST": 
        # Redirect to create new poll
        if "new_poll" in request.form:
            session.pop("poll_id", None)
            return redirect(url_for("index"))
        
        if "preference" in request.form:
            preference = request.form.get("preference")
            if preference:
                session["voted"] = True       
                db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES (%s, %s, %s);", (seq, preference, 1))
                return redirect(url_for("result", seq=seq))
        else:
            error_select="Please select a pub."
            return redirect(url_for("result", seq=seq, error=error_select))
        

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        # Get data from form
        name = request.form.get("name")
        address = request.form.get("address")
        web = request.form.get("web")

        # Check if all fields are filled in
        if not name or not address or not web:
            return render_template("add.html", message="Please fill in all fields.")
        
        # Check if pub already in database
        pub_list = db_conn.execute_query("SELECT name FROM pubs", fetchall=True)
        for pub in pub_list:
            if name == pub[0]:
                message = "Pub already in database."
                return render_template("add.html", message=message)
        
        # Insert data into database
        db_conn.execute_query("INSERT INTO pubs (name, address, web) VALUES (%s, %s, %s);", (name, address, web))
        
        return redirect(url_for("index"))

    return render_template("add.html")


if __name__ == '__main__':
    app.run(debug=True)