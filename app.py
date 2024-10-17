from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime
import uuid, bcrypt, os

app = Flask(__name__)
app.secret_key = "sdiusahdioasbfsdopjsdoifioiowesfiso"
db = sqlite3.connect("dreams_db.sqlite", check_same_thread=False)
cursor = db.cursor()


def dummy_user():
    session["username"] = "dreamer1"
    session["user_id"] = "ed03a10d-6e9e-442d-a318-7f21f31ebcde"

def get_profile_picture(user_id):
    if user_id is None:
        return None
    exts = ["png", "jpg", "jpeg", "gif", "webp", "jfif"]
    for ext in exts:
        if os.path.exists(f"{user_id}.{ext}"):
            return f"{user_id}.{ext}"
    return "default.jpg"

def get_session_info():
    #dummy_user()
    if "username" in session:
        username = session.get("username")
        user_id = session.get("user_id")
    else:
        username = None
        user_id = None
    
    return username, user_id

@app.route("/")
def dreambrowse():
    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)

    author_id_to_name = {}

    with db:
        cursor.execute("SELECT * FROM dreams WHERE private = 0 ORDER BY upload_date DESC;")
        dreams = cursor.fetchall()
        
        author_ids = set()
        for dream in dreams:
            author_ids.add(dream[4])
        
        for author_id in author_ids:
            cursor.execute("SELECT username FROM users WHERE user_id = ?", (author_id,))
            author_id_to_name[author_id] = cursor.fetchone()[0]
    
    
    return render_template(
        "dream_browser.html", dreams=dreams, author_id_to_name=author_id_to_name, username=username, user_id=user_id, profile_pic=profile_pic
    )

@app.route("/dream/<dream_id>")
def dream(dream_id):

    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)

    with db:
        cursor.execute("SELECT * FROM dreams WHERE dream_id = ?", (dream_id,))
        dream = cursor.fetchone()
        if dream is None:
            return "Dream not found", 404
        else:
            content = dream[1]
            title = dream[2]
            description = dream[3]
            author_id = dream[4]
            tag = dream[5]
            upload_date = dream[6]
            upload_date = datetime.strptime(upload_date, "%Y-%m-%d")
            upload_date = upload_date.strftime("%d.%m.%Y")
            # likes = dream[8] im not using this yet (maybe never)

            cursor.execute("SELECT username FROM users WHERE user_id = ?", (author_id,))
            author_name = cursor.fetchone()[0]

    if user_id == author_id:
        user_is_author = True
    else:
        user_is_author = False

    return render_template(
        "dream.html",
        dream_id=dream_id,
        id=dream_id,
        title=title,
        content=content,
        author=author_name,
        tag=tag,
        upload_date=upload_date,
        description=description,
        user_is_author=user_is_author,
        username=username,
        user_id=user_id,
        profile_pic=profile_pic,
    )

@app.route("/dream", methods=["POST", "GET"])
def dreams():
    username, user_id = get_session_info()
    
    if username is None:
        return redirect(url_for("login"))
    
    profile_pic = get_profile_picture(user_id)
    
    if request.method == "POST":
        form = request.form
        
        with db:
            dream_id = str(uuid.uuid4())
            upload_date = datetime.now().strftime("%Y-%m-%d")
            
            try: 
                cursor.execute(
                    """
                    INSERT INTO dreams (dream_id, content, title, description, author_id, tag, upload_date, private)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (dream_id, form["content"], form["title"], form["description"], user_id, form["tag"], upload_date, form["private"]),
                )
            except:
                cursor.execute(
                    """
                    INSERT INTO dreams (dream_id, content, title, description, author_id, tag, upload_date, private)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                    """,
                    (dream_id, form["content"], form["title"], form["description"], user_id, form["tag"], upload_date, 0),
                )
            db.commit()

            return redirect(url_for("dream", dream_id=dream_id))

    return render_template(
        "new_dream.html", username=username, user_id=user_id, profile_pic=profile_pic
    )

@app.route("/delete/<dream_id>")
def delete(dream_id):
    username, user_id = get_session_info()

    with db:
        if user_id is None:
            return "stop trying to delete a dream when not signed in", 403

        cursor.execute("SELECT author_id FROM dreams WHERE dream_id = ?", (dream_id,))
        author_id = cursor.fetchone()[0]
        cursor.execute("SELECT admin FROM users WHERE user_id = ?", (author_id,))
        admin = cursor.fetchone()[0]

        if author_id != user_id:
            return "stop trying to delete someone elses dream you bitch", 403

        if author_id == user_id or admin == 1:
            cursor.execute("DELETE FROM dreams WHERE dream_id = ?", (dream_id,))
            return redirect(url_for("dreams"))

@app.route("/profile/<author_id>")
def profile(author_id): # ill do this later, since its not MVP
    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)
    
    with db:
        if user_id == author_id:
            cursor.execute("SELECT * FROM dreams WHERE author_id = ?", (author_id,))
        else:
            cursor.execute("SELECT * FROM dreams WHERE author_id = ? AND private = 0", (author_id,))

        author_dreams = cursor.fetchall()
    
    return render_template('profile.html', username=username, user_id=user_id, profile_pic=profile_pic, author_dreams=author_dreams)

@app.route("/login", methods=['POST', 'GET'])
def login():
    username, user_id = get_session_info()

    if request.method == 'POST':
        if username is None:

            given_email = request.form.get('email')
            given_pass = request.form.get('password')
            err = None

            cursor.execute("""
                            SELECT hash FROM users WHERE email = ?;
                        """, (given_email,))
            
            result = cursor.fetchone()

            if result is None:
                err = "Incorrect email or password." 
            else:  
                stored_hash = result[0].encode("utf-8")

                if bcrypt.checkpw(given_pass.encode("utf-8"), stored_hash):
                    session["username"] = cursor.execute("""
                                        SELECT username FROM users WHERE email = ?;
                                        """, (given_email,)).fetchone()[0]
                    session["user_id"] =  cursor.execute("""
                                        SELECT user_id FROM users WHERE email = ?;
                                        """, (given_email,)).fetchone()[0]
                    return redirect(url_for("dreams"))
                else:
                    err = "Incorrect email or password."

            return render_template("log_in.html", err=err)
        else:
            return redirect(url_for("dreams"))
    else:
        return render_template("log_in.html", err=None)

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        with db:
            user_id = str(uuid.uuid4())

            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(form['password'].encode("utf-8"), salt)

            # Insert the user into the 'users' table
            cursor.execute(
                """
                INSERT INTO users (user_id, username, hash, email, admin)
                VALUES (?, ?, ?, ?, ?);
                """,
                (user_id, form['username'], password_hash.decode("utf-8"), form['email'], 0),
            )

            db.commit()

            session["username"] = form['username']
            session["user_id"] = user_id

            return redirect(url_for("dreams"))
        
    else:
        return render_template("register.html")

@app.route("/usernamechecker/<username>", methods=["GET"])
def usernamechecker(username):
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result is None:
        return "false"
    else:
        return "true"

@app.route("/emailchecker/<email>", methods=["GET"])
def emailchecker(email):
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    result = cursor.fetchone()
    if result is None:
        return "false"
    else:
        return "true"

@app.route("/terms")
def terms():
    return "terms of service"

@app.route("/privacy")
def privacy():
    return "privacy policy"

if __name__ == "__main__":
    # currently using a "fake user" session for testing
    app.run(debug=True)
