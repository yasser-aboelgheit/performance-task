from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from .factories import QuestionFactory, AnswerFactory
from .models import Choice, Answer, Question
from datetime import datetime


class TestPassengerAPIView(APITestCase):
    def setUp(self):
        self.login_credentials = {
            'username': 'test1', 'password': 'testpassword'}
        self.user = User.objects.create_user(
            **self.login_credentials, is_staff=True)
        self.url = reverse('answers')
        self.login_url = reverse('token_obtain_pair')
        login_response = self.client.post(
            self.login_url, self.login_credentials)
        token = login_response.data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        self.question = QuestionFactory.create()
        self.question2 = QuestionFactory.create()
        self.answer = AnswerFactory.create(
            question=self.question, choice=self.question.choices.last())
        self.answer2 = AnswerFactory.create(
            question=self.question2, choice=self.question2.choices.first())
        self.answer2.created_at = datetime(2021, 3, 1)
        self.answer2.save()

    def test_success_return(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_credential_provided(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get("detail"),
                         "Authentication credentials were not provided.")

    def test_superuser_user(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get("detail"),
                         "You do not have permission to perform this action.")

    def test_not_staff_user(self):
        self.user.is_staff = False
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get("detail"),
                         "You do not have permission to perform this action.")

    def test_dates(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        answer_dates = list(Answer.objects.values_list("created_at", flat=True))
        response_answer_dates = [*response.json()[0]] + [*response.json()[1]]
        self.assertEqual(response_answer_dates.sort(), answer_dates.sort())

    def test_questions_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date_of_answer = str(self.answer.created_at)
        questions_count = Question.objects.filter(answers__created_at=date_of_answer).distinct().count()
        date_of_answer_content = [i for i in response.json() if list(i.keys())[0] == date_of_answer]
        self.assertEqual(date_of_answer_content[0]["2021-03-28"][1].get("questions_count"), questions_count)

    def test_question_text(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date_of_answer = str(self.answer.created_at)
        question = Question.objects.filter(answers__created_at=date_of_answer).distinct().last()
        date_of_answer_content = [i for i in response.json() if list(i.keys())[0] == date_of_answer]
        question_text = (list(date_of_answer_content[0].get('2021-03-28')[0].keys()))[0]
        self.assertEqual(question_text, question.text)

    def test_question_answers_count(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date_of_answer = str(self.answer.created_at)
        question = Question.objects.filter(answers__created_at=date_of_answer).distinct().last()
        date_of_answer_content = [i for i in response.json() if list(i.keys())[0] == date_of_answer]
        answers_count = date_of_answer_content[0].get('2021-03-28')[0][question.text]['answers'][1].get('answers_count')
        self.assertEqual(answers_count, question.answers.count())

    def test_question_answers_id(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date_of_answer = str(self.answer.created_at)
        question = Question.objects.filter(answers__created_at=date_of_answer).distinct().last()
        answer = Answer.objects.filter(question=question).last()
        date_of_answer_content = [i for i in response.json() if list(i.keys())[0] == date_of_answer]
        answer_id = date_of_answer_content[0].get('2021-03-28')[0][question.text]['answers'][0].get("id")
        self.assertEqual(answer_id, answer.id)

    def test_question_answers_content(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        date_of_answer = str(self.answer.created_at)
        question = Question.objects.filter(answers__created_at=date_of_answer).distinct().last()
        answer = Answer.objects.filter(question=question).last()
        date_of_answer_content = [i for i in response.json() if list(i.keys())[0] == date_of_answer]
        answer_content = date_of_answer_content[0].get('2021-03-28')[0][question.text]['answers'][0]
        self.assertEqual(answer_content.get("choice").get("text"), answer.choice.text)
        self.assertEqual(answer_content.get("choice").get("id"), answer.choice.id)
