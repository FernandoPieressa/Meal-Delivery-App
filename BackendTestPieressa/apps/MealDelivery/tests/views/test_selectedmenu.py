import uuid
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from ...models.selectedmenu import SelectedMenu
from ...models.employee import Employee

class TestChooseMealView(TestCase):
    """Tests for the choose meal view"""
    def setUp(self):
        employee = Employee.objects.create(username='username',
                                           name='name')
        self.selected_menu = SelectedMenu.objects.create(user=employee, date=date.today())
        self.client = Client()
        self.choose_meal_url = reverse('MealDelivery:choose_meal', kwargs={
            'id': self.selected_menu.id
        })

    def test_view_unexisting_choose_meal_view(self):
        """User can't access unexisting view"""
        choose_meal_url = reverse('MealDelivery:choose_meal', kwargs={
            'id': str(uuid.uuid4())
        })

        response = self.client.get(choose_meal_url)
        self.assertEqual(response.status_code, 404)

    def test_choose_meal_view_get(self):
        """User can access the choose meal view correctly"""

        response = self.client.get(self.choose_meal_url)
        self.assertTemplateUsed(response, 'MealDelivery/components/models/choose_delivery.html')
        self.assertEqual(response.status_code, 200)
