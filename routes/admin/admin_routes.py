from flask import (
    Blueprint,
    flash,
    render_template,
    redirect,
    request,
    session,
    url_for,
)

from utils.upstash import upstash
from .admin_utils import AddUserForm, AddWeightForm
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

    if not add_user_form.validate_on_submit():
        session["form_errors"] = add_user_form.errors
    
    else:
        username = add_user_form.username.data
        password = add_user_form.password.data
        # Verify connection
        if upstash.redis is None:
            flash("Not connected to Upstash")
            logger.error("Upstash Redis connection is None")
        # Verift not existing
        elif upstash.get_user(username):
            flash(f"User already exists: {username}")
            logger.info(f"User already exists: {username=}")
        # Add user
        else:
            upstash.add_user(username, password)
            flash(f"Added user: {username}")
                
        return redirect(url_for(CFG.redirect.add_user))
    
    form_errors = session.pop("form_errors", None)

    return render_template(
        CFG.template.add_user,
        title="Add user",
        add_user_form=add_user_form,
        form_errors=form_errors,
        url=CFG.redirect.add_user,
    )


@admin_bp.route(CFG.route.add_weight, methods=["GET", "POST"])
@login_required
@admin_required
def add_weight():
    """Displays add weight form."""
    add_weight_form = AddWeightForm()
    
    if not add_weight_form.validate_on_submit():
        session["form_errors"] = add_weight_form.errors
    
    else:
        date = add_weight_form.date.data
        weight = float(add_weight_form.weight.data)
        existing_weight = upstash.get_weight(date)
        # Verify connection
        if upstash.redis is None:
            flash("Not connected to Upstash")
            logger.error("Upstash Redis connection is None")
        # Verify not existing
        elif existing_weight:
            flash(f"Weight already exists: {date}")
            logger.info(f"Weight already exists: {date}: {existing_weight}")
        # Add weight
        else:
            upstash.add_weight(weight, date)
            flash(f"Added weight: {date}: {weight}")
            logger.info(f"Added weight: {date=} {weight=}")
        
        return redirect(url_for(CFG.redirect.add_weight))
    
    form_errors = session.pop("form_errors", None)
    
    return render_template(
        CFG.template.add_weight,
        title="Add Weight",
        add_weight_form=add_weight_form,
        form_errors=form_errors,
        url=CFG.redirect.add_weight,
    )
