from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask_login import current_user
from datetime import date, datetime, timedelta
import calendar
from app.models import Equipment, User, Event
from app.main.forms import EventForm, EquipmentForm
from app import db

main = Blueprint('main', __name__)
timeslots = [
    "09:00-11:00",
    "11:00-13:00",
    "13:00-15:00",
    "15:00-17:00"
]
@main.route('/')
def home():
    """Display all events and users in kanban calendar."""
    return redirect(url_for('main.get_calendar', date_input = datetime.now().strftime('%Y-%m-%d')))

@main.route('/get_calendar/<date_input>')
def get_calendar(date_input):
    """Returns current state of the calendar"""
    equipment = Equipment.query.all()
    month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]))
    prev_month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]) - 1)
    date_current = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
    date_next = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) + 1 if int(date_input[8:10]) < month_range[1] else 1)
    date_prev = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) - 1 if int(date_input[8:10]) > 1 else prev_month_range[1])
    all_equipment = []
    for item in equipment:
        temp = Equipment(
            name = item.name, 
            quantity = item.quantity,
        )
        temp.id = str(item.id)
        temp.events = temp.get_events(date_input)
        all_equipment.append(temp)
    context = {
        "timeslots": timeslots,
        "is_empty": len(all_equipment) == 0,
        "all_equipment": all_equipment,
        "date": str(date_current.month) + "/" + str(date_current.day),
        "date_full": date_input,
        "date_next": date_next.strftime('%Y-%m-%d'),
        "date_prev": date_prev.strftime('%Y-%m-%d')
    }
    return render_template('calendar.html', **context)


@main.route('/new_event/<equipment_id>/<date_input>/<timeslot>', methods=['GET', 'POST'])
def new_event(equipment_id, date_input, timeslot):
    """Display the event creation page & process data from the creation form."""
    form = EventForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            event = Event(
                title = form.title.data,
                color = form.color.data,
                date = form.date.data,
                timeslot = form.timeslot.data,
                user = current_user, #User(id= 3, username= "hi", password= "password"),
                equipment = form.equipment.data
            )
            db.session.add(event)
            db.session.commit()
            flash('Event Created.')
        print(form.errors)
        return redirect(url_for('main.home'))
    else:
        context = {
            "timeslot_input": timeslot,
            "date_input": date_input,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        form.date.default = date_input
        form.timeslot.default = timeslot
        form.equipment.default = [equipment_id]
        print(form.errors)
        return render_template('new_event.html', form=form)

@main.route('/new_equipment', methods=['GET', 'POST'])
def new_equipment():
    """Display the equipment creation page & process data from the creation form."""
    form = EquipmentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            equipment = Equipment(
                name = form.name.data,
                quantity = form.quantity.data
            )
            db.session.add(equipment)
            db.session.commit()
            flash('Equipment Created.')
        print(form.errors)
        return redirect(url_for('main.home'))
    else:
        print(form.errors)
        return render_template('new_equipment.html', form=form)
