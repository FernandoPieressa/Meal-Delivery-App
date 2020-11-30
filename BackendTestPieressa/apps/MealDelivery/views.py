from datetime import date, datetime
import threading
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import EmployeeForm, MealFormset, DateForm, SelectedMenuForm
from .models import Meal, SelectedMenu, Employee

def send_slack_reminder(employee, meal_date, host, protocol):
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

@login_required(login_url='MealDelivery:login')
def home(request):
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
        employees = Employee.objects.all()
        host = request.get_host()
        protocol = request.scheme
        thread_list = []
        for employee in employees:
            reminder_thread = threading.Thread(
                target=send_slack_reminder,
                args=(employee, current_date, host, protocol,)
            )
            thread_list.append(reminder_thread)
        for thread in thread_list:
            thread.start()
    return render(request, 'MealDelivery/home.html', {
        'meal_choices': meal_choices,
        'day_choices': day_choices,
        'date': current_date,
        'date_form': date_form,
        'error_msg': error_msg
        })

@login_required(login_url='MealDelivery:login')
def add_menu(request):
    error_msg = None
    current_date = date.today()
    date_form = DateForm({'date': current_date})
    template_name = 'MealDelivery/add_menu.html'
    if request.method == 'GET':
        formset = MealFormset(request.GET or None)
    elif request.method == 'POST':
        formset = MealFormset(request.POST)
        date_form = DateForm(request.POST)
        if formset.is_valid() and date_form.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                menu_date = date_form.cleaned_data.get('date')
                if name:
                    Meal(name=name, date=menu_date).save()
            return redirect('MealDelivery:index')
        error_msg = 'Date must be valid'
    return render(request, template_name, {
        'formset': formset,
        'date_form': date_form,
        'error_msg': error_msg
    })

@login_required(login_url='MealDelivery:login')
def delete_meal(request, id):
    meal = Meal.objects.get(id=id)
    meal.delete()
    return redirect('MealDelivery:index')

def choose_meal(request, id):
    current_time = datetime.now()
    template_name = 'MealDelivery/choose_delivery.html'
    selected_menu = SelectedMenu.objects.get(id=id)
    if int(current_time.strftime('%H')) >= 11:
        selected_menu.expired = True
        selected_menu.save()
        return render(request, template_name, {
            'expired': True
        })
    if request.method == 'POST':
        selected_menu.meal = Meal.objects.get(id=request.POST['meal'])
        selected_menu.customization = request.POST['customization']
        selected_menu.save()
        return render(request, template_name, {
            'finished': True,
            'expired': False
        })
    possible_meals = Meal.objects.filter(date=selected_menu.date)
    possible_meals_choices = [(possible_meal.id, possible_meal.name)
                              for possible_meal in possible_meals]
    selected_menu_form = SelectedMenuForm(possible_meals_choices)
    return render(request, template_name, {
        'selected_menu_form': selected_menu_form,
        'date': selected_menu.date,
        'finished': False,
        'expired': False
    })

@login_required(login_url='MealDelivery:login')
def add_employee(request):
    employees = Employee.objects.all()
    if request.method == 'POST':
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            employee_form.save()
            return redirect('MealDelivery:index')
    else:
        employee_form = EmployeeForm()
    return render(request, 'MealDelivery/add_employee.html', {
        'employee_form': employee_form,
        'employees': employees
    })

@login_required(login_url='MealDelivery:login')
def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MealDelivery:login')
    context = {'form': form}
    return render(request, 'MealDelivery/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('MealDelivery:index')
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('MealDelivery:index')
        context['message'] = 'Username or password is incorrect'
    return render(request, 'MealDelivery/login.html', context)

@login_required(login_url='MealDelivery:login')
def logout_user(request):
    logout(request)
    return redirect('MealDelivery:login')
