from datetime import date
from django.test import TestCase
from ...models.employee import Employee
from ...models.selectedmenu import SelectedMenu
from ...models.meal import Meal
from ..helpers.validations import is_valid_uuid

class SelectedMenuModelTestCase(TestCase):
    """Test for the selected menu model"""
    def setUp(self):
        self.date = date.today()
        self.username = 'username'
        self.name = 'name'
        self.customization = 'customization'
        self.expired = False
        self.user = Employee(username=self.username, name=self.name)
        self.meal = Meal(date=self.date, name=self.name)


    def test_persistance(self):
        """Selected menu model must maintain data persistance"""
        selected_menu = SelectedMenu(
            date=self.date,
            customization=self.customization,
            expired=self.expired,
            user=self.user,
            meal=self.meal,
            )
        self.assertEqual(selected_menu.date, self.date)
        self.assertEqual(selected_menu.customization, self.customization)
        self.assertEqual(selected_menu.expired, self.expired)
        self.assertEqual(selected_menu.user, self.user)
        self.assertEqual(selected_menu.meal, self.meal)
        self.assertEqual(is_valid_uuid(selected_menu.id), True)
