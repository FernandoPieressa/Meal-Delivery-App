from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        run_seed(self)

def run_seed(self):
    user = User(username='administrator')
    user.set_password('123456123a')
    user.save()
