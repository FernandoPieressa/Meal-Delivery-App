from django.db import models

class Meal(models.Model):
    """A class model that defines meals."""
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    name = models.CharField(max_length=100)

    class Meta:
        """A class metadata for the meal model."""
        verbose_name = 'Meal'
        verbose_name_plural = 'Meals'
        ordering = ['date']
