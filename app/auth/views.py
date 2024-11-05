from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.auth.models import User
import bcrypt
from app.utils import get_session_info


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    username, user_id = get_session_info()

    if request.method == "POST":
        if username is None:

            given_email = request.form.get("email")
            given_pass = request.form.get("password")
            err = None

            hash = User.query.with_entities(User.hash).filter_by(email=given_email).first()
            hash = hash[0] if hash else None
            
            if hash is None:
                err = "Incorrect email or password."
            else:
                stored_hash = hash[0].encode("utf-8")

                if bcrypt.checkpw(given_pass.encode("utf-8"), stored_hash):
                    session["username"] = User.query.with_entities(User.username).filter_by(email=given_email).first()[0]
                    session["user_id"] = User.query.with_entities(User.user_id).filter_by(email=given_email).first()[0]
                    return redirect(url_for("dreams"))
                else:
                    err = "Incorrect email or password."

            return render_template("log_in.html", err=err)
        else:
            return redirect(url_for("dreams"))
    else:
        return render_template("log_in.html", err=None)


@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    # Your existing registration code.
    pass

@auth_bp.route("/logout")
def logout():
    # Your existing logout code.
    pass
