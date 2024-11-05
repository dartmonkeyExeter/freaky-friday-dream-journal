from flask import session
import os

def get_session_info():
    if "username" in session:
        username = session.get("username")
        user_id = session.get("user_id")
    else:
        username = None
        user_id = None
    return username, user_id

def get_profile_picture(user_id):
    if user_id is None:
        return None
    exts = ["png", "jpg", "jpeg", "gif", "webp", "jfif"]
    for ext in exts:
        if os.path.exists(f"{user_id}.{ext}"):
            return f"{user_id}.{ext}"
    return "default.jpg"