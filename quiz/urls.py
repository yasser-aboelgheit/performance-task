from django.urls import path
from .views import AnswerAPIView

urlpatterns = [
    path('answers/', AnswerAPIView.as_view(), name='answers'),
]
