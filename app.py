from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = "sdiusahdioasbfsdopjsdoifioiowesfiso"
db = sqlite3.connect("dreams_db.sqlite", check_same_thread=False)
cursor = db.cursor()


def dummy_user():
    session["username"] = "dreamer1"
    session["user_id"] = "ed03a10d-6e9e-442d-a318-7f21f31ebcde"


def get_session_info():
    # dummy_user()
    if "username" in session:
        username = session.get("username")
        user_id = session.get("user_id")
    else:
        username = None
        user_id = None
    return username, user_id


@app.route("/dreams/<dream_id>")
def dream(dream_id):

    username, user_id = get_session_info()

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
    )


@app.route("/dreams")
def dreams():

    username, user_id = get_session_info()

    with db:
        cursor.execute("SELECT * FROM dreams WHERE private = 0")
        dreams = cursor.fetchall()
    return render_template(
        "dreams.html", dreams=dreams, username=username, user_id=user_id
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


@app.route("/login")
def login():
    return "test"


if __name__ == "__main__":
    # currently using a "fake user" session for testing
    app.run(debug=True)
