from flask import Blueprint, request, redirect, render_template, url_for
from datetime import date, datetime, timedelta
import calendar
from app.models import Equipment, User, Event

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
    events = Event.query.all()
    equipment = Equipment.query.all()
    month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]))
    prev_month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]) - 1)
    date_current = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
    date_next = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) + 1 if int(date_input[8:10]) < month_range[1] else 1)
    date_prev = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) - 1 if int(date_input[8:10]) > 1 else prev_month_range[1])
    all_equipment = []
    if len(equipment) == 0:
        equipment = [
            {
                "id": 1,
                "name": "Wow",
                "quantity": 7
            },
            {
                "id": 2,
                "name": "Woa",
                "quantity": 12
            },
        ]
    for item in equipment:
        temp = Equipment(
            name = item['name'], 
            quantity = item['quantity'],
        )
        temp.id = str(item['id'])
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


@main.route('/new_event/<user_id>/<date_input>/<timeslot>', methods=['GET', 'POST'])
def new_event(user_id, date_input, timeslot):
    """Display the event creation page & process data from the creation form."""
    if request.method == 'POST':
        new_event = Event(
            request.form['title'],
            ObjectId(request.form['user']),
            request.form['color'],
            request.form['details'],
            request.form['date'],
            request.form['timeslot']
        )

        res = database.events.insert_one(new_event.get_dict())
        new_event.set_id(res.inserted_id)
        return redirect(url_for('home'))

    else:
        context = {
            "user_id": ObjectId(user_id),
            "timeslot_input": timeslot,
            "date_input": date_input,
            "users": database.users.find(),
            "timeslots": timeslots,
            "min_date": datetime.now(),
            'max_date': datetime.now() + timedelta(days=25),
        }
        return render_template('new_event.html', **context)
