from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from polls.models import Question, Choice


class Command(BaseCommand):
    help = 'Generate fake data for questions and choices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--amount', default=10,
            type=int, help='[Optional] Number of questions to create',
        )

    def handle(self, *args, **options):
        fake = Faker()
        amount = options['amount']
        for _ in range(amount):
            question_text = fake.sentence()
            pub_date = fake.date_time_between(start_date='-30d', end_date='now')
            question = Question.objects.create(
                question_text=question_text,
                pub_date=pub_date,
            )
            choices_qty = fake.random_int(min=3, max=5)
            for _ in range(choices_qty):
                choice_text = fake.word()
                votes = fake.random_int(min=0, max=100)
                Choice.objects.create(
                    question=question,
                    choice_text=choice_text,
                    votes=votes,
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully created {amount} dummy questions and choices.'))
