from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.auth.models import User
import bcrypt
import uuid
from app.utils import get_session_info

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    username, user_id = get_session_info()

    if request.method == "POST":
        if username is None:
            given_email = request.form.get("email")
            given_pass = request.form.get("password")
            
            # Get the user's hash by email
            user = User.query.filter_by(email=given_email).first()

            if user and bcrypt.checkpw(given_pass.encode("utf-8"), user.hash.encode("utf-8")):
                session["username"] = user.username
                session["user_id"] = user.user_id
                return redirect(url_for("dreams"))
            else:
                flash("Incorrect email or password.")  # Use flash for error messages

        return redirect(url_for("dreams"))
    else:
        return render_template("log_in.html", err=None)

@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        form = request.form
        user_id = str(uuid.uuid4())

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(form["password"].encode("utf-8"), salt)

        # Create a new user instance
        new_user = User(
            user_id=user_id,
            username=form["username"],
            email=form["email"],
            hash=password_hash.decode("utf-8"),  # Store the hash as a string
        )

        db.session.add(new_user)
        db.session.commit()

        session["username"] = form["username"]
        session["user_id"] = user_id

        return redirect(url_for("dreams"))
    else:
        return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    flash("You have been logged out.")  # Inform user of logout
    return redirect(url_for("auth.login"))  # Redirect to login page or homepage

@auth_bp.route("/usernamechecker/<username>", methods=["GET"])
def usernamechecker(username):
    result = User.query.filter_by(username=username).first()
    return "false" if result is None else "true"

@auth_bp.route("/emailchecker/<email>", methods=["GET"])
def emailchecker(email):
    result = User.query.filter_by(email=email).first()
    return "false" if result is None else "true"

@auth_bp.route("/terms")
def terms():
    return "terms"

@auth_bp.route("/privacy")
def privacy():
    return "privacy"

@auth_bp.route("/forgot_password")
def forgot_password():
    return "forgotpassword"