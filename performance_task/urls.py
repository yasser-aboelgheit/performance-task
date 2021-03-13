
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('accounts.urls')),
    path('quiz/', include('quiz.urls')),
]
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

# for i in range(10):
#     Question.objects.create(text="BLABLA"+str(i))
# for q in Question.objects.all():
#     for i in range(10):
#         Answer.objects.create(question=q, choice=Choice.objects.first())