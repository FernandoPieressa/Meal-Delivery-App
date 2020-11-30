from django.urls import path, include

urlpatterns = [
    path('menu/', include(('apps.MealDelivery.urls', 'MealDelivery')))
]
