from django.urls import path
from .views import AnswerAPIView, AnswerAPIView2

urlpatterns = [
    path('answers/', AnswerAPIView.as_view(), name='answers'),
    path('answers2/', AnswerAPIView2.as_view(), name='answers2'),
]
