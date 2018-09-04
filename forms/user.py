from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import (DataRequired, Email, Regexp, AnyOf, Length,
                                Optional)

from tzhelper import get_timezones


class UserForm(FlaskForm):
    """Flask WTF form to validate input"""
    name = StringField('name', validators=[DataRequired()])
    email = StringField(
        'email', validators=[Email(), Optional(strip_whitespace=True)])
    receive_marketing = BooleanField(
        'receive_marketing', validators=[Optional(strip_whitespace=True)])
    timezone = StringField(
        'timezone', validators=[DataRequired(),
                                AnyOf(get_timezones())])
    external_id = StringField(
        'external_id',
        validators=[Optional(strip_whitespace=True),
                    Length(min=14, max=14)])
    # tested at https://regex101.com/r/Lg2riP/1
    skills = StringField(
        'skills',
        validators=[
            Optional(strip_whitespace=True),
            Regexp(r"^(([a-zA-Z]+[a-zA-Z0-9 -]*)(, )?)+$")
        ])
