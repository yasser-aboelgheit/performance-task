from django.contrib import admin
from .models import Choice, Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(Answer, AnswerAdmin)