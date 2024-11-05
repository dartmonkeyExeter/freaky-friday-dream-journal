from flask import Blueprint

# Import the blueprint from views.py
from .views import dreams_bp

# Optionally, you could import any models if needed for ease of use
from .models import Dream

# __all__ can be used to specify the public interface of this package
__all__ = ['dreams_bp', 'Dream']
