from datetime import datetime, timedelta

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .home_utils import (
    WeightGuessForm,
    get_insta_months_from_path,
    get_last_guess,
    get_months_from_path,
    get_insta_paths,
    get_insta_title,
    get_image_path,
    get_title,
    get_guess_color,
)
from utils.misc import login_required
from utils.upstash import upstash
from utils.logger import logger
from utils.config import CFG


home_bp = Blueprint("home", __name__)


@home_bp.route(CFG.route.home, methods=["GET"])
@login_required
def home():
    """Displays empty page."""
    trainings = upstash.get_trainings()
    url = CFG.redirect.home
    main_title = "Next"
    next_workout = "Sunday September 14th"
    secondary_title = "Previous"

    return render_template(
        CFG.template.home,
        trainings=trainings,
        main_title=main_title,
        next_workout=next_workout,
        secondary_title=secondary_title,
        url=url,
    )


@home_bp.route(CFG.route.weight, methods=["GET", "POST"])
@login_required
def weight():
    """Displays weight images and month selection."""
    weight_guess_form = WeightGuessForm()

    if not weight_guess_form.validate_on_submit():
        session["form_errors"] = weight_guess_form.errors
    
    else:
        weight = float(weight_guess_form.weight.data)
        username = session["username"]
        guess_date = datetime.now() + timedelta(days=1)
        date = guess_date.strftime("%Y-%m-%d")
        upstash.add_weight_guess(username, date, weight)
        flash("Nice guess!")
        return redirect(url_for(CFG.redirect.weight))
    
    # Get data
    guess_date, guess_weight = get_last_guess(session["username"])
    guess_result = upstash.get_weight(guess_date)
    logger.info(f"username: {session['username']}, Guess date: {guess_date}, Guess weight: {guess_weight}, Guess result: {guess_result}")
    # Generate colored result
    guess_color = ""
    if guess_weight is not None and guess_result is not None:
        guess_color = get_guess_color(guess_weight, guess_result)
    
    form_errors = session.pop("form_errors", None)
    month = request.args.get('month')
    year = request.args.get('year')

    img_path = get_image_path(year, month, CFG.dir.WEIGHT_REL)
    title = get_title(img_path, month)
    all_months = get_months_from_path(CFG.dir.WEIGHT)
    url = CFG.redirect.weight
    
    return render_template(
        CFG.template.graph,
        title=title,
        img_path=img_path,
        all_months=all_months,
        selected_year=year,
        selected_month=month,
        url=url,
        weight_guess_form=weight_guess_form,
        form_errors=form_errors,
        guess_date=guess_date,
        guess_weight=guess_weight,
        guess_result=guess_result,
        guess_color=guess_color,
    )


@home_bp.route(CFG.route.calories, methods=["GET"])
@login_required
def calories():
    """Displays calories images and month selection."""
    month = request.args.get('month')
    year = request.args.get('year')
    
    img_path = get_image_path(year, month, CFG.dir.CALORIES_REL)
    title = get_title(img_path, month)
    all_months = get_months_from_path(CFG.dir.CALORIES)
    url = CFG.redirect.calories
    
    return render_template(
        CFG.template.graph,
        title=title,
        img_path=img_path,
        all_months=all_months,
        selected_year=year,
        selected_month=month,
        url=url,
    )


@home_bp.route(CFG.route.both, methods=["GET"])
@login_required
def both():
    """Displays calories and weight images and month selection."""
    month = request.args.get('month')
    year = request.args.get('year')
    
    img_path = get_image_path(year, month, CFG.dir.BOTH_REL)
    title = get_title(img_path, month)
    all_months = get_months_from_path(CFG.dir.BOTH)
    url = CFG.redirect.both
    
    return render_template(
        CFG.template.graph,
        title=title,
        img_path=img_path,
        all_months=all_months,
        selected_year=year,
        selected_month=month,
        url=url,
    )


@home_bp.route(CFG.route.insta, methods=["GET"])
@login_required
def insta():
    """Displays insta images and month selection."""
    month = request.args.get('month')
    year = request.args.get('year')

    left, back, front, right = get_insta_paths(year, month)
    title = get_insta_title(year, month)
    all_months = get_insta_months_from_path(CFG.dir.INSTA)
    url = CFG.redirect.insta

    return render_template(
        CFG.template.insta,
        img_left=left,
        img_back=back,
        img_front=front,
        img_right=right,
        title=title,
        all_months=all_months,
        selected_month=month,
        url=url,
    )
