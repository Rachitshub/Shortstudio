

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_from_directory,
    abort
)
import os
from werkzeug.utils import secure_filename
from config import Config
import psycopg

def init_db():
    conn = psycopg.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS videos (
        id SERIAL PRIMARY KEY,
        title TEXT,
        filename TEXT,
        category TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()
DB_URL=os.environ["DATABASE_URL"]
def get_db_con():
    return psycopg.connect(DB_URL)
    
 
app = Flask(__name__)


app.config.from_object(Config)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
app.secret_key = Config.SECRET_KEY
print("Upload folder:", app.config["UPLOAD_FOLDER"])
print(app.config["UPLOAD_FOLDER"])
@app.route("/")
def home():


    conn = get_db_con()
    cur = conn.cursor()

    cur.execute("SELECT * FROM videos ORDER BY id DESC")
    videos = cur.fetchall()

    conn.close()
    return render_template(
        "gallery.html",
        videos=videos
    )
    
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

# Create uploads folder if it doesn't exist
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(filepath)

            
            conn = get_db_con()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO videos (title, filename, category) VALUES (%s, %s, %s)",(title, filename, category))

            
            conn.commit()
            conn.close()

            return redirect("/gallery")

    return render_template("upload.html")
@app.route("/gallery")
def gallery():

    conn = get_db_con()
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
    
@app.route("/delete/<int:id>")
def delete_vid(id):
    if not session.get("admin"):
        abort(401) ;
    
    conn = get_db_con()
    cur = conn.cursor()
    cur.execute("SELECT filename FROM videos WHERE id=%s",(id,))
    filename = cur.fetchone()[0]
    if not filename :
        return abort(404)
    file = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    cur.execute("DELETE FROM videos WHERE id=%s",(id,))
    conn.commit()
    if  not os.path.exists(file):
        return abort(404)
    os.remove(file)
    conn.close()
    return redirect("/")
        
@app.route("/edit/<int:video_id>", methods=["GET", "POST"])
def edit(video_id):

    if not session.get("admin"):
        return redirect("/login")

    conn = get_db_con()
    cur = conn.cursor()

    if request.method == "POST":

        title = request.form["title"]
        category = request.form["category"]

        cur.execute(
            "UPDATE videos SET title=%s, category=%s WHERE id=%s",
            (title, category, video_id)
        )

        conn.commit()
        conn.close()

        return redirect("/gallery")

    cur.execute(
        "SELECT * FROM videos WHERE id=%s",
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

    conn = get_db_con()
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

    conn = get_db_con()
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
