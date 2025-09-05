from flask import (
    Blueprint,
    render_template,
    request,
)

from .home_utils import (
    get_insta_months_from_path,
    get_months_from_path,
    get_insta_paths,
    get_insta_title,
    get_image_path,
    get_title
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
