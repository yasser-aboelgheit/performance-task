from django.core.management.base import BaseCommand
from quiz.factories import QuestionFactory, AnswerFactory


class Command(BaseCommand):
    help = 'Create 10 questions and 1000 answers'

    def handle(self, *args, **kwargs):
        questions = QuestionFactory.create_batch(size=10)
        for i in range(10):
            AnswerFactory.create_batch(size=10, question=questions[i], choice=questions[i].choices.last())
        self.stdout.write("Created 10 questions and 1000 answers")