from rest_framework import generics
from .serializers import QuizReportSerializer
from .models import Answer, Question
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count, Q, F, Max
import json
from django.db.models import Prefetch
from django.db.models import Value, IntegerField, CharField
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from performance_task.permissions import IsNotSuperUserButStaff
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Value, DateField
from datetime import datetime
from silk.profiling.profiler import silk_profile
from itertools import groupby


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

        answers = Answer.objects.filter(
            **data).select_related("question", "choice").distinct()
        questions = (Question.objects.all(
        ).prefetch_related("answers").distinct())
        answer_dates = answers.values('created_at')
        # import ipdb;ipdb.set_trace()
        for date in answer_dates:
            date = date.get("created_at")
            question_dict = {}
            # questions_answered_on_date = questions.filter(answers__created_at=date).\
            #     values("answers__choice__id", "answers__choice__text", "answers__id", "text", "answers__created_at")

            # import ipdb;ipdb.set_trace()
            # questions_answered_on_date_count = questions_answered_on_date.count()
            # answers_text = [{o.get("text"): {"id": o.get("answers__id"),
            #                 "choice": {"id": o.get("answers__choice__id"), "text": o.get("answers__choice__text")}}}
            #                 for o in questions_answered_on_date]
            # ANOTHER APPROACH
            answers_nw = questions.filter(answers__created_at=date).distinct().annotate(
                answers_count=Count('answers'))
            # .prefetch_related(
            #      Prefetch(
            #     "answers",
            #     queryset=Answer.objects.filter(created_at=date)
            # ))
            # "answers").distinct()
            answers_content = [{k.text: [{"id": o.id,
                                          "choice": {"id": o.choice.id, "text": o.choice.text}}
                                         for o in k.answers.filter(created_at=date)],
                                "answers_count": k.answers_count} for k in answers_nw]
            # import ipdb;ipdb.set_trace()
            date_dict = {"questions_count": answers_nw.count()}
            # date_dict.update(question_dict)
            answers_content.append(date_dict)
            returned_data[str(date)] = answers_content

        return Response(returned_data)


class AnswerAPIView2(APIView):
    # permission_classes = [IsNotSuperUserButStaff]

    @silk_profile(name='View Blog Post')
    def get(self, request, format=None):
        serializer = QuizReportSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        returned_data = {}
        data = serializer.validated_data
        if data.get("from_date"):
            data["created_at__gte"] = data.pop("from_date")
        if data.get("to_date"):
            data["created_at__lte"] = data.pop("to_date")

        answers2 = Answer.objects.filter(
            **data)
        # questions = (Question.objects.all().prefetch_related("answers").distinct())
        answer_dates = answers2.values_list('created_at', flat=True).distinct()
        print(answer_dates)
        # import ipdb;ipdb.set_trace()
        # Now I have questions of specific dates and their answers including choice
        questions = (Question.objects.filter(answers__created_at__in=answer_dates)
                     .prefetch_related(Prefetch("answers",
                                                queryset=Answer.objects.all().
                                                select_related("choice"),
                                                to_attr="some_answers"))
                     .annotate(answers_count=Count('answers'))
                     .annotate(question_answered_at=Max("answers__created_at")).order_by("question_answered_at"))
        # for date in answer_dates:

        #  annotate(question_answered_at=Value(, DateField())))
        # questions = questions.annotate(question_answered_at=Max("answers__created_at"))
        # questions., DateField())
        # answers_text = [{o.get("text"): {"id": o.get("answers__id"),
        #     "choice": {"id": o.get("answers__choice__id"), "text": o.get("answers__choice__text")}}}
        #     for o in questions]
        # if o.created_at == k.question_answered_at
        answers_content = [{k.text: {"answers_count": k.answers_count,
                                     "answers": [{"id": o.id,
                                                  "choice": {"id": o.choice.id, "text": o.choice.text}}
                                                 for o in k.some_answers]},
                            "question_answered_at": k.question_answered_at} for k in questions]
        # print(answers_content)

        # answers_content = answers_content.sort("question_answered_at")
        answers_content.sort(key=lambda x: x['question_answered_at'])

        final = {}
        for key, value in groupby(answers_content, key=lambda x: x['question_answered_at']):
            value = list(value)
            value[0]["questions_count"] = len(value)
            value[0].pop("question_answered_at")
            # import ipdb
            # ipdb.set_trace()
            final[str(key)] = value
        # for key, value in final.items():
        #     value[0]["questions_count"] = len(value)
        #     print(value)
            # print(key)
            # print(list(value))
        # for key, value in hi:
        #     print(key, value)
        # strftime('%Y-%m-%d %H:%M')

        # answers_content = [{k.text: [{"id": o.id,
        #                        "choice": {"id": o.choice.id, "text": o.choice.text}}
        #                         for o in k.answers.filter(created_at=date)],
        #                         "answers_count": k.answers_count} for k in answers_nw]
        # for k in questions:
        #     print(k.some_answers[0].choice.text)
        # for date in answer_dates:
        #     date = date.get("created_at")
        #     question_dict = {}
        #     # questions_answered_on_date = questions.filter(answers__created_at=date).\
        #     #     values("answers__choice__id", "answers__choice__text", "answers__id", "text", "answers__created_at")
        #     # import ipdb;ipdb.set_trace()
        #     # questions_answered_on_date_count = questions_answered_on_date.count()
        #     # answers_text = [{o.get("text"): {"id": o.get("answers__id"),
        #     #                 "choice": {"id": o.get("answers__choice__id"), "text": o.get("answers__choice__text")}}}
        #     #                 for o in questions_answered_on_date]
        #     # ANOTHER APPROACH
        #     answers_nw = questions.filter(answers__created_at=date).distinct().annotate(answers_count=Count('answers'))
        #     # .prefetch_related(
        #     #      Prefetch(
        #     #     "answers",
        #     #     queryset=Answer.objects.filter(created_at=date)
        #     # ))
        #     # "answers").distinct()
        #     answers_content = [{k.text: [{"id": o.id,
        #                        "choice": {"id": o.choice.id, "text": o.choice.text}}
        #                         for o in k.answers.filter(created_at=date)],
        #                         "answers_count": k.answers_count} for k in answers_nw]
        #     # import ipdb;ipdb.set_trace()
        #     date_dict = {"questions_count": answers_nw.count()}
        #     # date_dict.update(question_dict)
        #     answers_content.append(date_dict)
        #     returned_data[str(date)] = answers_content

        return Response(final)

        # Sh5ala zay el fol
        # Now I have questions of specific dates and their answers including choice + answers_count

        # questions = (Question.objects.filter().prefetch_related(Prefetch("answers",
        #                                                               queryset=Answer.objects.all().\
        #                                                               select_related(
        #                                                                              "choice",
        #                                                               ),
        #                                                               to_attr="some_answers")).\
        #              annotate(answers_count=Count('answers')))
