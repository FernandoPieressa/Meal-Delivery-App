from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms.date import DateForm
from ..forms.meal import MealFormset
from ..models.meal import Meal

@login_required(login_url='MealDelivery:login')
def menu(request):
    """Users can access the menu form. Users can add multiple meals for a menu
    given a specific date. If date is invalid user receives an error message.
    If process is correct user is redirected to home view.

    Args:
        request (object): request given to the view

    Returns:
        redirect: render user to the view home
    """
    error_msg = None
    current_date = date.today()
    date_form = DateForm({'date': current_date})
    template_name = 'MealDelivery/components/models/menu.html'

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
    """Deletes a meal from the system.

    Args:
        request (object): request given to the view
        id (string): id of the meal to remove

    Returns:
        redirect: redirect user to the view home view
    """
    meal = Meal.objects.get(id=id)
    meal.delete()
    return redirect('MealDelivery:index')
