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

    if request.method == "POST":

        if not add_user_form.validate_on_submit():
            session["form_errors"] = add_user_form.errors
        
        else:
            username = add_user_form.username.data
            if upstash.get_user(username):
                logger.info(f"User already exists: {username=}")
                flash(f"User already exists: {username}")
            
            else:
                password = add_user_form.password.data
                added = upstash.add_user(username, password)
                if not added:
                    flash(f"Upstash not connected: {username}")
                    logger.error(f"Erorr adding user to Upstash: {username=}")
                    return redirect(url_for(CFG.redirect.add_user))

                logger.info(f"Added user: {username=}")
                flash(f"Added user: {username}")
            
            return redirect(url_for(CFG.redirect.add_user))
    
    url = CFG.redirect.add_user
    
    return render_template(
        CFG.template.add_user,
        title="Add user",
        add_user_form=add_user_form,
        url=url,
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
        logger.info(f"Trying to add weight: {date=} {weight=}")

        weight = upstash.get_weight(date)
        if weight:
            logger.info(f"Weight already exists: {date}: {weight}")
            flash(f"Weight already exists: {date}")
        
        else:
            added = upstash.add_weight(weight, date)
            if not added:
                flash(f"Upstash not connected: {date}")
            else:
                flash(f"Added weight: {date}: {weight}")
        
        return redirect(url_for(CFG.redirect.add_weight))
    
    
    url = CFG.redirect.add_weight
        
    return render_template(
    CFG.template.add_weight,
    title="Add Wwight",
    add_weight_form=add_weight_form,
    url=url,
    )
