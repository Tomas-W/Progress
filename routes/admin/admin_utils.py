from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from datetime import datetime


def validate_date_format(form, field):
    """Checks for YYYY-MM-DD date format"""
    try:
        datetime.strptime(field.data, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Must be YYYY-MM-DD")


class AddUserForm(FlaskForm):
    username = StringField(
        label="Username",
        render_kw={"placeholder": "Username"},
        validators=[
            DataRequired(message="Username is required"),
        ]
    )
    password = StringField(
        label="Password",
        render_kw={"placeholder": "Password"},
        validators=[
            DataRequired(message="Password is required"),
        ],
    )
    password2 = StringField(
        label="Repeat Password",
        render_kw={"placeholder": "Repeat Password"},
        validators=[
            DataRequired(message="Password is required"),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    form_type = HiddenField(default="add_user")
    submit = SubmitField(label="Add")


class AddWeightForm(FlaskForm):
    date = StringField(
        label="Date",
        render_kw={"placeholder": "YYYY-MM-DD"},
        validators=[
            DataRequired(message="Date is required"),
            validate_date_format,
        ],
    )
    weight = FloatField(
        label="Weight",
        render_kw={"placeholder": "Weight"},
        validators=[
            DataRequired(message="Weight is required"),
        ],
    )
    form_type = HiddenField(default="add_weight")
    submit = SubmitField(label="Add")
