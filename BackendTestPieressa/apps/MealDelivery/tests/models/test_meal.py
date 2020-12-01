from datetime import date
from django.test import TestCase
from ...models.meal import Meal

class MealModelTestCase(TestCase):
    """Test for the meal model"""
    def setUp(self):
        self.date = date.today()
        self.name = 'name'

    def test_persistance(self):
        """Meal model must maintain data persistance"""
        meal = Meal(date=self.date, name=self.name)
        self.assertEqual(meal.date, self.date)
        self.assertEqual(meal.name, self.name)
