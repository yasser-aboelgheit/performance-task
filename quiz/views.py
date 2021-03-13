from rest_framework import generics
from .serializers import QuizReportSerializer
from .models import Answer, Question
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, F
import json
from django.db.models import Prefetch
from django.db.models import Value, IntegerField, CharField
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from performance_task.permissions import IsNotSuperUserButStaff
class AnswerAPIView(APIView):
    permission_classes = [IsNotSuperUserButStaff]
    def get(self, request, format=None):
        serializer = QuizReportSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        returned_data = {}
        data = serializer.validated_data
        if data.get("from_date"):
            data["created_at__gte"] = data.pop("from_date")
        if data.get("to_date"):
            data["created_at__lte"] = data.pop("to_date")

        # print(data)
        # print(filter(**data))
        # queryset = Export.objects.filter().order_by("-created_at")
        answers = Answer.objects.filter(**data).select_related("question", "choice").distinct()
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
