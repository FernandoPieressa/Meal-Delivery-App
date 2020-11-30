from datetime import date
import threading
import requests
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from ..forms.date import DateForm
from ..models.selectedmenu import SelectedMenu
from ..models.meal import Meal
from ..models.employee import Employee

def send_single_slack_reminder(employee, meal_date, host, protocol):
    """Creates a selected model object to create the unique url the employee
    has to use to choose a meal. Then sends a slack reminder to the specific
    employee.

    Args:
        employee (Employee): employee to send slack reminder
        meal date (date): date of the meal
        host (string): hostname of the django application
        protocol (string): protocol of the django application (http/https)
    """
    daily_menu = SelectedMenu(user=employee, date=meal_date)
    daily_menu.save()
    message_text = (
        "Remember to choose today's meal! "+protocol+'://'+host+'/menu/'
        +str(daily_menu.id)
    )
    payload = {
        'token': settings.SLACK_TOKEN,
        'text': message_text,
        'time': 60,
        'user': employee.username
    }
    requests.post('https://slack.com/api/reminders.add', data=payload)

def send_all_slack_reminders(host, protocol, current_date):
    """Sends a slack reminder to every single employee of the application.
    As this uses Django 3.0.5 and async isn't available on views, it creates a
    thread for every single employee to publish reminder.

    Args:
        host (string): hostname of the django application
        protocol (string): protocol of the django application (http/https)
        current_date (date): date of the meal
    """
    employees = Employee.objects.all()
    thread_list = []
    for employee in employees:
        reminder_thread = threading.Thread(
            target=send_single_slack_reminder,
            args=(employee, current_date, host, protocol,)
        )
        thread_list.append(reminder_thread)
    for thread in thread_list:
        thread.start()

@login_required(login_url='MealDelivery:login')
def home(request):
    """Home view of the application. Users can view the menu of specific dates
    and total meal selected for each plate and remove meals from menu.
    Users can also send reminder to all employees given a specific date and
    see the employees selections afterward.

    Args:
        request (object): request given to the view

    Returns:
        render: render user to the view home
    """
    error_msg = None
    current_date = request.GET.get('date', date.today())
    date_form = DateForm({'date': current_date})

    if not date_form.is_valid():
        current_date = date.today()
        date_form = DateForm({'date': current_date})
        error_msg = 'Date must be valid'

    day_meals = Meal.objects.filter(date=current_date)
    day_choices = SelectedMenu.objects.filter(date=current_date)
    meal_choices = [(SelectedMenu.objects.filter(
        date=current_date, meal=meal).count(), meal) for meal in day_meals]

    if request.method == 'POST':
        host = request.get_host()
        protocol = request.scheme
        send_all_slack_reminders(host, protocol, current_date)
    return render(request, 'MealDelivery/components/home.html', {
        'meal_choices': meal_choices,
        'day_choices': day_choices,
        'date': current_date,
        'date_form': date_form,
        'error_msg': error_msg
        })
