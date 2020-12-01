from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required(login_url='MealDelivery:login')
def register_view(request):
    """Registers new user to the website so it can manage the meal delivery
    system. To create a new user you must be logged in with a current user.

    Args:
        request (object): request given to the view

    Returns:
        redirect: render user to the login view
    """
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('MealDelivery:login')
    return render(request, 'MealDelivery/components/session/register.html',
                  {'form': form})

def login_view(request):
    """Login user to the application. Only logged users can use most of the
    app's functionalities.

    Args:
        request (object): request given to the view

    Returns:
        redirect: render user to the home view
    """
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

    return render(request, 'MealDelivery/components/session/login.html',
                  context)

@login_required(login_url='MealDelivery:login')
def logout_user(request):
    """Logout user from the application.

    Args:
        request (object): request given to the view

    Returns:
        redirect: render user to the login view
    """
    logout(request)
    return redirect('MealDelivery:login')
