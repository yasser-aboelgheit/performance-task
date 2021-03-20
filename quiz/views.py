from rest_framework import generics
from .serializers import QuizReportSerializer
from .models import Answer, Question
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
import json
from django.db.models import Prefetch
from performance_task.permissions import IsNotSuperUserButStaff
from django.contrib.postgres.aggregates import ArrayAgg
from datetime import datetime
from silk.profiling.profiler import silk_profile


class AnswerAPIViewOld(APIView):
    permission_classes = [IsNotSuperUserButStaff]

    @silk_profile(name='AnswerAPIView Old')
    def get(self, request, format=None):
        serializer = QuizReportSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        returned_data = {}
        data = serializer.validated_data
        if data.get("from_date"):
            data["created_at__gte"] = data.pop("from_date")
        if data.get("to_date"):
            data["created_at__lte"] = data.pop("to_date")

        answers = Answer.objects.filter(
            **data).select_related("question", "choice").distinct()
        questions = (Question.objects.all(
        ).prefetch_related("answers").distinct())
        answer_dates = answers.values('created_at')
        for date in answer_dates:
            date = date.get("created_at")
            question_dict = {}
            answers_nw = questions.filter(answers__created_at=date).distinct().annotate(
                answers_count=Count('answers'))
            answers_content = [{k.text: [{"id": o.id,
                                          "choice": {"id": o.choice.id, "text": o.choice.text}}
                                         for o in k.answers.filter(created_at=date)],
                                "answers_count": k.answers_count} for k in answers_nw]
            date_dict = {"questions_count": answers_nw.count()}
            answers_content.append(date_dict)
            returned_data[str(date)] = answers_content

        return Response(returned_data)


class AnswerAPIView(APIView):
    permission_classes = [IsNotSuperUserButStaff]

    @silk_profile(name='AnswerAPIView optimized')
    def get(self, request, format=None):
        serializer = QuizReportSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        returned_data = {}
        data = serializer.validated_data
        if data.get("from_date"):
            data["created_at__gte"] = data.pop("from_date")
        if data.get("to_date"):
            data["created_at__lte"] = data.pop("to_date")

        answers2 = Answer.objects.filter(**data)
        answer_dates = answers2.values_list('created_at', flat=True).distinct()
        questions_dates = {}
        for date in answer_dates:
            questions = (Question.objects.filter(answers__created_at=date)
                         .prefetch_related(Prefetch("answers",
                                                    queryset=Answer.objects.filter(created_at=date).
                                                    select_related("choice").defer(
                                                        "updated_at"),
                                                    to_attr="question_answers"))
                         .annotate(answers_count=Count('answers')))
            questions_dates[str(date)] = questions

        answers_content = [{date: ([{question.text: {
            "answers": [{"id": answer.id,
                         "choice": {"id": answer.choice.id, "text": answer.choice.text}}
                        for answer in question.question_answers] + [{"answers_count": question.answers_count}]},
        } for question in questions] + [{"questions_count": questions.count()}]
        )} for date, questions in questions_dates.items()]
        return Response(answers_content)
