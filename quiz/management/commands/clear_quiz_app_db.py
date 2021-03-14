from django.core.management.base import BaseCommand
from quiz.models import Question, Answer, Choice


class Command(BaseCommand):
    help = 'Clear Database from questions, answers and choices'

    def handle(self, *args, **kwargs):
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Choice.objects.all().delete()
        self.stdout.write("Cleared Database from questions, answers and choices")