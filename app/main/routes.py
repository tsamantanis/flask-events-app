from flask import Blueprint, request, redirect, render_template, url_for
from datetime import date, datetime, timedelta
import calendar

main = Blueprint('main', __name__)

@main.route('/')
def home():
    """Display all events and users in kanban calendar."""
    return redirect(url_for('main.get_calendar', date_input = datetime.now().strftime('%Y-%m-%d')))

@main.route('/get_calendar/<date_input>')
def get_calendar(date_input):
    """Returns current state of the calendar"""
    # users = database.users.find()
    # user_list = []
    # for user in users:
    #     a_user = user(user['first_name'], user['last_name'], user['email'])
    #     id = user['_id']
    #     a_user.set_id(str(id))
    #     a_user.get_events(date_input)
    #     user_list.append(a_user)
    month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]))
    prev_month_range = calendar.monthrange(int(date_input[0:4]), int(date_input[5:7]) - 1)
    date_current = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]))
    date_next = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) + 1 if int(date_input[8:10]) < month_range[1] else 1)
    date_prev = date(int(date_input[0:4]), int(date_input[5:7]), int(date_input[8:10]) - 1 if int(date_input[8:10]) > 1 else prev_month_range[1])
    context = {
        "timeslots": [], # timeslots,
        "is_empty": True, # len(user_list) == 0,
        "user_list": [], # user_list,
        "date": str(date_current.month) + "/" + str(date_current.day),
        "date_full": date_input,
        "date_next": date_next.strftime('%Y-%m-%d'),
        "date_prev": date_prev.strftime('%Y-%m-%d')
    }
    return render_template('calendar.html', **context)