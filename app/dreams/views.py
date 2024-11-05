from flask import Blueprint, render_template, request, url_for, session
from app.extensions import db
from app.dreams.models import Dream
from app.auth.models import User
import uuid
from datetime import datetime
from app.utils import get_session_info, get_profile_picture

dreams_bp = Blueprint("dreams", __name__, url_prefix="/dreams")

@dreams_bp.route("/dream/<dream_id>")
def dream(dream_id):

    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)

    dream = Dream.query.filter(Dream.dream_id == dream_id).first()

    if dream is None:
        return "Dream not found", 404
    else:
        content = dream.content
        title = dream.title
        description = dream.description
        author_id = dream.author_id
        tag = dream.tag
        upload_date = dream.upload_date.strftime("%d.%m.%Y")
        # likes = dream[8] im not using this yet (maybe never)

        author = User.query.filter(User.user_id == author_id).first()
        author_name = author.username if author else "Unknown"


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

@dreams_bp.route("/profile/<author_id>")
def profile(author_id):  # ill do this later, since its not MVP
    username, user_id = get_session_info()
    profile_pic = get_profile_picture(user_id)

    if user_id == author_id:
        author_dreams = Dream.query.filter(Dream.author_id == author_id).all()
    else:
        author_dreams = Dream.query.filter((Dream.author_id == author_id) & (Dream.private == False)).all()

    return render_template(
        "profile.html",
        username=username,
        user_id=user_id,
        profile_pic=profile_pic,
        author_dreams=author_dreams,
    )