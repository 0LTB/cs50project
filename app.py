from flask import Flask, render_template, request, redirect, url_for
from helpers import db_conn, str_generator as str_gen



app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    # Generate string for session unique URL
    seq = str_gen.create_sequence()

    if request.method == "POST":
        voted = request.form.get("preference")
        db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES  (%s, %s, %s);", (seq, voted, 1))
        return redirect(url_for("result", seq=seq))

    pubs_list = db_conn.execute_query("SELECT * FROM pubs ORDER BY name;", fetchall=True)
    return render_template("index.html", pubs_list=pubs_list, seq=seq)

@app.route("/result/<seq>", methods=["GET", "POST"])
def result(seq):

    if request.method == "GET":
        pubs_list = db_conn.execute_query("SELECT pubs.id, name, address, web, COALESCE(sum, 0), polls.id\
                                  FROM (SELECT id, pubs_id, SUM(polls.vote)\
                                  FROM polls\
                                  WHERE polls.id = %s\
                                  GROUP BY id, pubs_id) polls\
                                  RIGHT JOIN pubs ON pubs_id = pubs.id\
                                  ORDER BY sum DESC;", (seq, ), fetchall=True)
        return render_template("result.html", pubs_list=pubs_list, seq=seq)

    if request.method == "POST":
        preference = request.form.get("preference")
        db_conn.execute_query("INSERT INTO polls (id, pubs_id, vote) VALUES (%s, %s, %s);", (seq, preference, 1))
        print(f"Redirecting to result with seq: {seq}")  # Debugging print statement
        return redirect(f"/result/{seq}")




if __name__ == '__main__':
    app.run(debug=True)