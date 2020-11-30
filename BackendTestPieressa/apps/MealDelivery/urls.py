from django.urls import path
from .views import home, add_menu, add_employee, delete_meal, choose_meal, \
    login_view, register_view, logout_user

urlpatterns = [
    path('home', home, name='index'),
    path('add_menu', add_menu, name='add_menu'),
    path('add_employee', add_employee, name='add_employee'),
    path('delete_meal/<int:id>', delete_meal, name='delete_meal'),
    path('login', login_view, name='login'),
    path('register', register_view, name='register'),
    path('logout', logout_user, name='logout'),
    path('<str:id>', choose_meal, name='choose_meal')
]
