from django.test import TestCase
from ...models.employee import Employee

class EmployeeModelTestCase(TestCase):
    """Test for the employee model"""
    def setUp(self):
        self.username = 'username'
        self.name = 'name'

    def test_persistance(self):
        """Employee model must maintain data persistance"""
        employee = Employee(username=self.username, name=self.name)
        self.assertEqual(employee.username, self.username)
        self.assertEqual(employee.name, self.name)
