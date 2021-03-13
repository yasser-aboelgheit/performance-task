from rest_framework import serializers
from .models import Answer, Choice, Question
import datetime
import iso8601
from django.core.exceptions import ValidationError
from dateutil import parser


class QuizReportSerializer(serializers.Serializer):
    from_date = serializers.CharField(required=False)
    to_date = serializers.CharField(required=False)
    zeby = serializers.SerializerMethodField(read_only=True)

    def validate_from_date(self, value):
        try:
            return (parser.parse(value))
        except:
            raise ValidationError({'message': 'Please enter a valid start date'})

    def validate_to_date(self, value):
        try:
            return (parser.parse(value))
        except:
            raise ValidationError({'message': 'Please enter a valid end date'})
