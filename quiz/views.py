from rest_framework import generics
from .serializers import AnswerSerializer, OutputSerializer
from .models import Answer, Question
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, F
import json
from django.db.models import Prefetch
from django.db.models import Value, IntegerField, CharField

class AnswerAPIView(APIView):

    def get(self, request, format=None):
        returned_data = {}
        answers = Answer.objects.all().select_related("question", "choice").distinct()
        questions = Question.objects.all().prefetch_related("answers", "answers__choice").distinct()
        answer_dates = answers.values_list('created_at', flat=True)

        for date in answer_dates:
            questions_answered_on_date = Question.objects.filter(answers__created_at=date).distinct()
            questions_answered_on_date_count = questions_answered_on_date.count()
            question_dict = {}
            for question in questions_answered_on_date:
                question_answers = Answer.objects.filter(question=question, created_at=date)
                answers = question_answers.values("choice__id", "choice__text", "id")
                answers_text = ({"id": o.id,
                                "choice": {"id": o.choice.id, "text": o.choice.text}
                                 } for o in question_answers)
                question_dict[question.text] = {"answers_count": answers.count(),
                                                "answers": answers_text}
            date_dict = {"questions_count": questions_answered_on_date_count}
            date_dict.update(question_dict)
            returned_data[str(date)] = [date_dict]

        return Response(returned_data)
