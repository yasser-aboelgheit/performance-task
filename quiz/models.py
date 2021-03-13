from django.db import models


class Choice(models.Model):
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text


class Question(models.Model):
    text = models.TextField()
    choices = models.ManyToManyField(Choice, related_name="questions")

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="answers")
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.question.text + " | " + self.choice.text
