from django.urls import path
from .views import SelfRegisterViewSet, MakeSuperUserViewSet

urlpatterns = [
    path('register/', SelfRegisterViewSet.as_view(), name='register'),
    path('upgrade-super-user/', SelfRegisterViewSet.as_view(), name='upgrade_super_user'),
]
