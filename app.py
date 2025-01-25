from flask import Flask, render_template, request, redirect, session, url_for
from helpers import db_conn, str_generator as str_gen



app = Flask(__name__)
app.config["DEBUG"] = True

app.secret_key = str_gen.create_sequence()

@app.route("/", methods=["GET", "POST"])
def index():
    # Generate string for session unique URL
    seq = str_gen.create_sequence()

    if request.method == "POST":
        voted = request.form.get("preference")
        db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES  (%s, %s, %s);", (seq, voted, 1))
        session["voted"] = True
        return redirect(url_for("result", seq=seq))

    pubs_list = db_conn.execute_query("SELECT * FROM pubs ORDER BY name;", fetchall=True)
    return render_template("index.html", pubs_list=pubs_list, seq=seq)

@app.route("/result/<seq>", methods=["GET", "POST"])
def result(seq):
    
    if request.method == "GET":
        pubs_list = db_conn.execute_query("SELECT pubs.id,\
                                        pubs.name,\
                                        pubs.address,\
                                        pubs.web,\
                                        COALESCE(polls.sum, 0) AS total_votes,\
                                        polls.id \
                                        FROM (\
                                          SELECT polls.id, \
                                          pubs_id, SUM(polls.vote) AS sum\
                                          FROM polls\
                                          WHERE polls.id = %s\
                                          GROUP BY polls.id, pubs_id\
                                        ) polls\
                                        RIGHT JOIN pubs ON pubs.id = polls.pubs_id\
                                        ORDER BY total_votes DESC;", (seq, ), fetchall=True)
        return render_template("result.html", pubs_list=pubs_list, seq=seq)

    if request.method == "POST":
        preference = request.form.get("preference")
        if preference:
            session["voted"] = True       
            db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES (%s, %s, %s);", (seq, preference, 1))
            return redirect(url_for("result", seq=seq))
        else:
            return redirect(url_for("index"))




if __name__ == '__main__':
    app.run(debug=True)