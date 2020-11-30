import uuid
from django.db import models

class SelectedMenu(models.Model):
    """A class model that defines employee's meal choice from menu."""
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
        """A class metadata for the SelectedMenu model."""
        verbose_name = 'SelectedMenu'
        verbose_name_plural = 'SelectedMenus'
        ordering = ['date']
