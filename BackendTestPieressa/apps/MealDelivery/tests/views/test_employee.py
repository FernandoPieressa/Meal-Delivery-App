from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ...models.employee import Employee

class TestEmployeeView(TestCase):
    """Tests for the employee view"""
    def setUp(self):
        self.client = Client()
        self.employee_url = reverse('MealDelivery:add_employee')

    def test_employee_not_logged_user(self):
        """User should be redirected if tried to get into the view without
        logging in"""
        response = self.client.get(self.employee_url)

        self.assertEqual(response.status_code, 302)

    def test_employee_get(self):
        """Should render employee template if logged user"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')
        response = self.client.get(self.employee_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'MealDelivery/components/models/employee.html')

    def test_employee_post(self):
        """Should add new employee if post method"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.post(self.employee_url, {
            'username': 'username',
            'name': 'name'
        })

        created_employee = Employee.objects.get(username='username')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(created_employee.username, 'username')
        self.assertEqual(created_employee.name, 'name')

    def test_employee_post_invalid(self):
        """Should render employee view if invalid creation"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.post(self.employee_url, {})

        self.assertEqual(response.status_code, 200)

class TestDeleteEmployeeView(TestCase):
    """Tests for the delete employee view"""
    def setUp(self):
        self.client = Client()
        self.employee = Employee.objects.create(username='username',
                                                name='name')
        self.delete_employee_url = reverse('MealDelivery:delete_employee',
                                           kwargs={'id': 'username'})

    def test_delete_employee_not_logged_user(self):
        """User should not be able to delete employee if not logged in"""
        response = self.client.post(self.delete_employee_url)

        created_employee = Employee.objects.get(username='username')

        self.assertEqual(response.status_code, 302)
        self.assertTrue(created_employee)

    def test_delete_employee_post(self):
        """User should be able to delete employee if logged in"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        response = self.client.post(self.delete_employee_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Employee.objects.all().count(), 0)

    def test_delete_unexisting_employee_post(self):
        """User can't remove unexisting employee"""
        User.objects.create_user(username='username',
                                 password='password')
        self.client.login(username='username', password='password')

        delete_employee_url = reverse('MealDelivery:delete_employee',
                                      kwargs={'id': 'fakeid'})

        response = self.client.post(delete_employee_url)
        self.assertEqual(response.status_code, 404)
