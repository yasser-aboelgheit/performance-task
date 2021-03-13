from rest_framework import serializers
from .models import Answer, Choice, Question


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = "__all__"

class OutputSerializer(serializers.Serializer):
    text = serializers.CharField()
    answers_count = serializers.CharField()
    answers = serializers.SerializerMethodField(required=False)

    def get_answers(self, obj):
        return AnswerSerializer(Answer.objects.filter(question=obj), many=True).data