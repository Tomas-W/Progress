from flask import (
    Blueprint,
    render_template,
    request,
)
from typing import Final

from .home_utils import (
    get_calories_months,
    get_insta_months,
    get_weight_months,
    get_calories_path,
    get_insta_paths,
    get_insta_title,
    get_weight_path,
    _get_title
)
from utils.misc import login_required
from utils.config import CFG
from utils.logger import logger


home_bp = Blueprint("home", __name__)


@home_bp.route(CFG.route.home, methods=["GET"])
@login_required
def home():
    """Displays empty page."""
    return render_template(
        CFG.template.home,
    )


@home_bp.route(CFG.route.weight, methods=["GET"])
@login_required
def weight():
    """Displays weight images and month selection."""
    month = request.args.get('month')
    year = request.args.get('year')
    
    img_path = get_weight_path(year, month)
    title = _get_title(img_path, month)
    all_months = get_weight_months()
    url = CFG.redirect.weight
    
    return render_template(
        CFG.template.graph,
        title=title,
        img_path=img_path,
        all_months=all_months,
        selected_year=year,
        selected_month=month,
        url=url,
    )


@home_bp.route(CFG.route.calories, methods=["GET"])
@login_required
def calories():
    """Displays calories images and month selection."""
    month = request.args.get('month')
    year = request.args.get('year')
    
    img_path = get_calories_path(year, month)
    title = _get_title(img_path, month)
    all_months = get_calories_months()
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


@home_bp.route(CFG.route.insta, methods=["GET"])
@login_required
def insta():
    """Displays insta page."""
    month = request.args.get('month')
    year = request.args.get('year')
    
    left, body, right = get_insta_paths(year, month)
    title = get_insta_title(year, month)
    all_months = get_insta_months()
    url = CFG.redirect.insta

    return render_template(
        CFG.template.insta,
        img_left=left,
        img_body=body,
        img_right=right,
        title=title,
        all_months=all_months,
        selected_month=month,
        url=url,
    )
