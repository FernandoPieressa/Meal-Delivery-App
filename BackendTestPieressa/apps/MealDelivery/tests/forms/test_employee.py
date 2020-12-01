from django.test import TestCase
from ...forms.employee import EmployeeForm

class EmployeeFormTestCase(TestCase):
    """Tests for EmployeeForm"""
    def test_employee_form_valid_data_type(self):
        """form must accept valid data types"""
        date_form = EmployeeForm(data={
            'username': 'username',
            'name': 'name'
        })

        self.assertTrue(date_form.is_valid())

    def test_employee_form_missing_data(self):
        """form must fail if missing data"""
        date_form = EmployeeForm(data={
            'username': 'username',
        })

        self.assertFalse(date_form.is_valid())
        self.assertEqual(len(date_form.errors), 1)
