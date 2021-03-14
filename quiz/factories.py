import factory
from faker import Factory
from .models import Choice, Question, Answer
faker = Factory.create()


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Choice

    text = factory.Faker('text')


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    text = factory.Faker('text')

    @factory.post_generation
    def choices(self, create, extracted, **kwargs):
        if create:
            for _ in range(4):
                self.choices.add(ChoiceFactory())


class AnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answer

    question = factory.SubFactory(QuestionFactory)
    choice = factory.SubFactory(ChoiceFactory)
