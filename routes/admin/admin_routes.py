from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    url_for,
)

from utils.upstash import upstash
from .admin_utils import AddUserForm
from utils.misc import login_required, admin_required
from utils.logger import logger
from utils.config import CFG


admin_bp = Blueprint("admin", __name__)


@admin_bp.route(CFG.route.add_user, methods=["GET", "POST"])
@login_required
@admin_required
def add_user():
    """Displays add user form."""
    add_user_form = AddUserForm()

    if add_user_form.validate_on_submit():
        username = add_user_form.username.data
        password = add_user_form.password.data
        logger.info(f"Trying to add user: {username=} {password=}")

        if upstash.get_user(username):
            logger.info(f"User already exists: {username=}")
            flash(f"User already exists: {username}")
        else:
            upstash.add_user(username, password)
            logger.info(f"Added user: {username=}")
            flash(f"Added user: {username}")
        
        return redirect(url_for("admin.add_user"))
    
    return render_template(
        CFG.template.add_user,
        title="Add User",
        add_user_form=add_user_form,
    )
