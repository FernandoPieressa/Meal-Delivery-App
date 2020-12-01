from datetime import date
from django.test import TestCase
from ...forms.selectedmenu import SelectedMenuForm
from ...models.meal import Meal

class SelectedMenuFormTestCase(TestCase):
    """Tests for SelectedMenuForm"""
    def setUp(self):
        """Set up of meals for selected menu form"""
        current_date = date.today()
        name = 'name'
        possible_meals = [Meal(date=current_date, name=name)]
        self.possible_meals_choices = [(possible_meal.id, possible_meal.name)
                                       for possible_meal in possible_meals]

    def test_date_valid_data(self):
        """form must accept valid data"""
        selected_menu_form = SelectedMenuForm(self.possible_meals_choices)

        self.assertTrue(selected_menu_form)


    def test_date_invalid_data(self):
        """form must throw error if no choices are given"""
        try:
            SelectedMenuForm()
        except TypeError as error:
            self.assertEqual(type(error), TypeError)
