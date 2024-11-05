from flask import Blueprint, render_template, request, redirect, url_for, session
from app.extensions import db
from app.auth.models import User
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["POST", "GET"])
def login():
    # Your existing login code.
    pass

@auth_bp.route("/register", methods=["POST", "GET"])
def register():
    # Your existing registration code.
    pass

@auth_bp.route("/logout")
def logout():
    # Your existing logout code.
    pass
