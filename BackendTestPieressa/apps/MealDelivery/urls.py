from django.urls import path
from .views.employee import employee, delete_employee
from .views.session import login_view, register_view, logout_user
from .views.meal import menu, delete_meal
from .views.home import home
from .views.selectedmenu import choose_meal

urlpatterns = [
    path('home', home, name='index'),

    path('add_menu', menu, name='add_menu'),
    path('delete_meal/<int:id>', delete_meal, name='delete_meal'),

    path('add_employee', employee, name='add_employee'),
    path('delete_employee/<str:id>', delete_employee, name='delete_employee'),

    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_user, name='logout'),

    path('<str:id>', choose_meal, name='choose_meal')
]
