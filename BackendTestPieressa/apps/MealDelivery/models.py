import uuid
from django.db import models

class Meal(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        ordering = ['date']

class Employee(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['name']

class SelectedMenu(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date = models.DateField()
    customization = models.TextField(blank=True, null=True)
    expired = models.BooleanField(default=False)
    user = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE
    )
    meal = models.ForeignKey(
        'Meal',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'SelectedMenu'
        verbose_name_plural = 'SelectedMenus'
        ordering = ['date']
