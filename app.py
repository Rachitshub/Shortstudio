

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_from_directory
)

import os
import sqlite3
from werkzeug.utils import secure_filename
from config import Config


app = Flask(__name__)
from config import Config

app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        filename TEXT,
        category TEXT,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()
@app.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos ORDER BY id DESC")
    videos = cur.fetchall()

    conn.close()

    return redirect("/gallery")

    return render_template("index.html", videos=videos)
@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "rachit" and password == "rptl":
            session["admin"] = True
            return redirect("/dashboard")
        else:
            error = "Invalid Username or Password"

    return render_template("login.html", error=error)
@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/login")

    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
@app.route("/upload", methods=["GET", "POST"])
def upload():

    if not session.get("admin"):
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]

        file = request.files["video"]

        if file:

            filename = secure_filename(file.filename)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO videos(title,filename,category) VALUES(?,?,?)",
                (title, filename, category)
            )

            conn.commit()
            conn.close()

            return redirect("/gallery")

    return render_template("upload.html")
@app.route("/gallery")
def gallery():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos ORDER BY id DESC")

    videos = cur.fetchall()

    conn.close()

    return render_template(
        "gallery.html",
        videos=videos
    )
@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
@app.route("/edit/<int:video_id>", methods=["GET", "POST"])
def edit(video_id):

    if not session.get("admin"):
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]

        cur.execute(
            "UPDATE videos SET title=?, category=? WHERE id=?",
            (title, category, video_id)
        )

        conn.commit()
        conn.close()

        return redirect("/gallery")

    cur.execute(
        "SELECT * FROM videos WHERE id=?",
        (video_id,)
    )

    video = cur.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        video=video
    )
@app.route("/search")
def search():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos ORDER BY title ASC")

    videos = cur.fetchall()

    conn.close()

    return render_template(
        "search.html",
        videos=videos
    )


@app.route("/category")
def category():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos ORDER BY category ASC")

    videos = cur.fetchall()

    conn.close()

    return render_template(
        "category.html",
        videos=videos
    )
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
