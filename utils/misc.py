import os

from flask import session, redirect, url_for, flash, request
from functools import wraps

from utils.config import CFG


def login_required(f):
    """Redirects to login page if user is not logged in."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if os.getenv("IS_LOCAL") == "Y":
            session["username"] = "admin"
            return f(*args, **kwargs)
        if "username" not in session:
            flash("You need to be logged in to access this page.")
            return redirect(url_for(CFG.redirect.landing, next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Redirects to home page if user is not admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if os.getenv("IS_LOCAL") == "Y":
            session["username"] = "admin"
            return f(*args, **kwargs)
        if session["username"] != "admin" and session["username"] != "test":
            flash("You need to be an admin to access this page.")
            return redirect(url_for(CFG.redirect.home))
        return f(*args, **kwargs)
    return decorated_function
