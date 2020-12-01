import threading
from mock import patch
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ...models.selectedmenu import SelectedMenu
from ...models.employee import Employee
from ...models.meal import Meal
from ...views.home import send_all_slack_reminders, send_single_slack_reminder

class TestHomeView(TestCase):
    """Tests for the home view"""
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('MealDelivery:index')

    def test_home_view_not_logged_user(self):
        """User should be redirected if tried to get into the view without
        logging in"""
        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 302)

    def test_home_view_get(self):
        """User should be able to see all menu and employee meal choices given
        a specific date"""

        employee = Employee.objects.create(username='username',
                                           name='name')

        current_date = date.today()

        meal = Meal.objects.create(date=current_date, name='name')

        selected_menu = SelectedMenu.objects.create(user=employee, date=current_date)

        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.get(self.home_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MealDelivery/components/home.html')
        self.assertEqual(response.context['meal_choices'], [(0, meal)])
        self.assertEqual(response.context['day_choices'][0].user, employee)

class TestSendSlackReminder(TestCase):
    """Tests for the send of slack reminder"""
    def setUp(self):
        self.host = 'localhost'
        self.protocol = 'http'
        self.date = date.today()

        self.employee = Employee.objects.create(username='username1',
                                                name='name')

    def test_send_single_slack_reminders(self):
        """It should send slack reminder to a single employee"""

        send_single_slack_reminder(self.employee,
                                   self.date, self.host, self.protocol)

        self.assertEqual(SelectedMenu.objects.filter(date=self.date).count(), 1)
