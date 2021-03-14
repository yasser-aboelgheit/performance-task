from django.core.management.base import BaseCommand
from quiz.factories import QuestionFactory, AnswerFactory


class Command(BaseCommand):
    help = 'Create 100 questions and 10000 answers'

    def handle(self, *args, **kwargs):
        questions = QuestionFactory.create_batch(size=100)
        for i in range(100):
            AnswerFactory.create_batch(size=100, question=questions[i], choice=questions[i].choices.last())
        self.stdout.write("Created 100 questions and 10000 answers")