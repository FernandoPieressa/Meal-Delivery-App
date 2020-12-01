from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views.employee import employee, delete_employee
from ..views.session import login_view, register_view, logout_user
from ..views.meal import menu, delete_meal
from ..views.home import home
from ..views.selectedmenu import choose_meal

class TestUrls(SimpleTestCase):
    """Test meal delivery application's urls"""

    def test_index_url_is_resolved(self):
        """Test index correct resolve from url"""
        url = reverse('MealDelivery:index')
        self.assertEqual(resolve(url).func, home)

    def test_add_menu_url_is_resolved(self):
        """Test add_menu correct resolve from url"""
        url = reverse('MealDelivery:add_menu')
        self.assertEqual(resolve(url).func, menu)

    def test_delete_meal_url_is_resolved(self):
        """Test delete_meal correct resolve from url"""
        url = reverse('MealDelivery:delete_meal', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, delete_meal)

    def test_add_employee_url_is_resolved(self):
        """Test add_employee correct resolve from url"""
        url = reverse('MealDelivery:add_employee')
        self.assertEqual(resolve(url).func, employee)

    def test_delete_employee_url_is_resolved(self):
        """Test delete_employee correct resolve from url"""
        url = reverse('MealDelivery:delete_employee', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, delete_employee)

    def test_login_url_is_resolved(self):
        """Test login correct resolve from url"""
        url = reverse('MealDelivery:login')
        self.assertEqual(resolve(url).func, login_view)

    def test_logout_url_is_resolved(self):
        """Test logout correct resolve from url"""
        url = reverse('MealDelivery:logout')
        self.assertEqual(resolve(url).func, logout_user)

    def test_register_url_is_resolved(self):
        """Test register correct resolve from url"""
        url = reverse('MealDelivery:register')
        self.assertEqual(resolve(url).func, register_view)

    def test_selectedmenu_url_is_resolved(self):
        """Test register correct resolve from url"""
        url = reverse('MealDelivery:choose_meal', kwargs={'id': 1})
        self.assertEqual(resolve(url).func, choose_meal)
