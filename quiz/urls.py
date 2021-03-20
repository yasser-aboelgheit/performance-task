from django.urls import path
from .views import AnswerAPIView, AnswerAPIViewOld

urlpatterns = [
    path('answers/', AnswerAPIView.as_view(), name='answers'),
    path('answers2/', AnswerAPIViewOld.as_view(), name='answers2'),
]
