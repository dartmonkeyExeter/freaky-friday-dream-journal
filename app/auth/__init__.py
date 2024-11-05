from flask import Blueprint

# Import the blueprint from views.py
from .views import auth_bp

# Optionally, import models if needed
from .models import User

# Specify the public interface of the package
__all__ = ['auth_bp', 'User']
