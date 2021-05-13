from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    FloatField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.fields.core import DateField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from app.models import Event, Equipment, User

class EventForm(FlaskForm):
    """Form for adding/updating a Event."""
    title = StringField("Title", validators=[DataRequired(), Length(min = 2, max = 80)])
    color = SelectField("Color", choices=[
        ("#00A88B", "#00A88B"),
        ("#307FE2", "#307FE2"),
        ("#6A6DCD", "#6A6DCD"),
        ("#C340A1", "#C340A1"),
        ("#D93535", "#D93535")
    ], validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired(), Length(min = 10, max = 10)]) # , format="%Y-%m-%d", validators=[DataRequired()])
    timeslot = SelectField("Timeslot", choices=[
        ("09:00-11:00", "09:00-11:00"),
        ("11:00-13:00", "11:00-13:00"),
        ("13:00-15:00", "13:00-15:00"),
        ("15:00-17:00", "15:00-17:00")
    ], validators=[DataRequired()])
    equipment = QuerySelectField('Equipment', query_factory=lambda: Equipment.query)
    # user = QuerySelectField('User', query_factory=lambda: User.query)
    submit = SubmitField("Submit")


class EquipmentForm(FlaskForm):
    """Form for adding/updating a Equipment."""
    name = StringField("Name", validators=[DataRequired(), Length(min = 2, max = 80)])
    quantity = FloatField("Quantity", validators=[DataRequired(), NumberRange(min = 1)])
    # event = QuerySelectField("Event", query_factory = lambda: Event.query, allow_blank = False)
    submit = SubmitField("Submit")
