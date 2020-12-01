from django.test import TestCase
from ...forms.meal import MealForm

class MealFormTestCase(TestCase):
    """Tests for MealForm"""
    def test_name_valid_data(self):
        """form must accept valid name"""
        meal_form = MealForm(data={
            'name': 'name',
        })

        self.assertTrue(meal_form.is_valid())

    def test_date_invalid_data(self):
        """form must fail if no name is given"""
        meal_form = MealForm(data={
        })

        self.assertFalse(meal_form.is_valid())
        self.assertEqual(len(meal_form.errors), 1)
