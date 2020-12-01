from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ...models.meal import Meal

class TestMenuView(TestCase):
    """Tests for the employee view"""
    def setUp(self):
        self.client = Client()
        self.current_date = date.today()
        self.menu_url = reverse('MealDelivery:add_menu')

    def test_menu_not_logged_user(self):
        """User should be redirected if tried to get into the view without
        logging in"""
        response = self.client.get(self.menu_url)

        self.assertEqual(response.status_code, 302)

    def test_menu_get(self):
        """Should render menu template if logged user"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')
        response = self.client.get(self.menu_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,
                                'MealDelivery/components/models/menu.html')

class TestDeleteMealView(TestCase):
    """Tests for the delete meal view"""
    def setUp(self):
        self.client = Client()
        self.meal = Meal.objects.create(date=date.today(), name='name')
        self.delete_meal_url = reverse('MealDelivery:delete_meal',
                                       kwargs={'id': self.meal.id})

    def test_delete_meal_not_logged_user(self):
        """User should not be able to delete meal if not logged in"""
        response = self.client.post(self.delete_meal_url)

        created_meal = Meal.objects.get(id=self.meal.id)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(created_meal)

    def test_delete_meal_post(self):
        """User should be able to delete employee if logged in"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.post(self.delete_meal_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Meal.objects.all().count(), 0)

    def test_delete_unexisting_meal_post(self):
        """User can't remove unexisting employee"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        delete_meal_url = reverse('MealDelivery:delete_meal',
                                  kwargs={'id': 123})

        response = self.client.post(delete_meal_url)
        self.assertEqual(response.status_code, 404)
