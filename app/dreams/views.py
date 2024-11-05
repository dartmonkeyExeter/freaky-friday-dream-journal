from flask import Blueprint, render_template, request, url_for, session
from app.extensions import db
from app.dreams.models import Dream
from app.auth.models import User
import uuid
from datetime import datetime

dreams_bp = Blueprint("dreams", __name__, url_prefix="/dreams")

@dreams_bp.route("/")
def dreambrowse():
    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)

    author_id_to_name = {}

    with db:
        if username:
            cursor.execute(
                "SELECT * FROM dreams WHERE private = 0 OR author_id = ? ORDER BY upload_date DESC;",
                (user_id,),
            )
        else:
            cursor.execute(
                "SELECT * FROM dreams WHERE private = 0 ORDER BY upload_date DESC;"
            )
        dreams = cursor.fetchall()

        author_ids = set()
        for dream in dreams:
            author_ids.add(dream[4])

        for author_id in author_ids:
            cursor.execute("SELECT username FROM users WHERE user_id = ?", (author_id,))
            author_id_to_name[author_id] = cursor.fetchone()[0]

    return render_template(
        "dream_browser.html",
        dreams=dreams,
        author_id_to_name=author_id_to_name,
        username=username,
        user_id=user_id,
        profile_pic=profile_pic,
    )

@dreams_bp.route("/dream/<dream_id>")
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