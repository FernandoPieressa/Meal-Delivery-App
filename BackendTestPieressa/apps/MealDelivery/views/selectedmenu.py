from datetime import datetime
from django.shortcuts import render
from ..forms.selectedmenu import SelectedMenuForm
from ..models.selectedmenu import SelectedMenu
from ..models.meal import Meal


def choose_meal(request, id):
    """Let employees choose a meal. Employees can select a meal from a menu and
    add customization options to it. If users try to choose or access the view
    after 11:00am CLP time the link expires. No authentification needed to
    access view.

    Args:
        request (object): request given to the view
        id (uuid): uuid of the selectedMenu to update with employee preferences

    Returns:
        render: render user to the view with status update
    """
    current_time = datetime.now()
    template_name = 'MealDelivery/components/models/choose_delivery.html'
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
