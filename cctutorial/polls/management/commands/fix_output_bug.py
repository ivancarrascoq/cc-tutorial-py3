from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fixes the output bug in the polls app'

    def handle(self, *args, **options):
        # logic here
        self.stdout.write(self.style.SUCCESS('Bug fixed successfully!'))
