from django.db import models

class Employee(models.Model):
    """A class model that defines employees."""
    username = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        """A class metadata for the employee model."""
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['name']
