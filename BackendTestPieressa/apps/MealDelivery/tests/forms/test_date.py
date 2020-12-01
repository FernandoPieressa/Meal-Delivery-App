from datetime import date
from django.test import TestCase
from ...forms.date import DateForm

class DateFormTestCase(TestCase):
    """Tests for DateForm"""
    def test_date_valid_data(self):
        """form must accept valid date"""
        date_form = DateForm(data={
            'date': date.today(),
        })

        self.assertTrue(date_form.is_valid())

    def test_date_invalid_data(self):
        """form must fail if invalid date"""
        date_form = DateForm(data={
            'date': 'invalid date',
        })

        self.assertFalse(date_form.is_valid())
        self.assertEqual(len(date_form.errors), 1)
