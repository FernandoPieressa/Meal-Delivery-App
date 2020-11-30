from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    """
    A custom command to add an administrator user that manages the
    meal delivery application.

    Methods
    -------
    handle()
        Runs the user seed
    """
    def handle(self, *args, **options):
        run_seed(self)

def run_seed(self):
    """Creates an administrator user to use the meal delivery application."""
    user = User(username='administrator')
    user.set_password('123456123a')
    user.save()
