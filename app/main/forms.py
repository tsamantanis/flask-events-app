from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    FloatField,
)
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from models import Event, Equipment, User

class EventForm(FlaskForm):
    """Form for adding/updating a Event."""
    title = StringField("Title", validators=[DataRequired(), Length(min = 2, max = 80)])
    equipment = QuerySelectMultipleField('Equipment', query_factory=lambda: Equipment.query)
    user = QuerySelectMultipleField('User', query_factory=lambda: User.query)
    submit = SubmitField("Submit")


class EquipmentForm(FlaskForm):
    """Form for adding/updating a Equipment."""
    name = StringField("Name", validators=[DataRequired(), Length(min = 2, max = 80)])
    quantity = FloatField("Quantity", validators=[DataRequired(), NumberRange(min = 1)])
    event = QuerySelectField("Event", query_factory = lambda: Event.query, allow_blank = False)
    submit = SubmitField("Submit")
