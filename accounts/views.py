from rest_framework import generics
from .serializers import UserSerializer, SuperUserSerializer
from django.contrib.auth.models import User

class SelfRegisterViewSet(generics.CreateAPIView):
    serializer_class = UserSerializer

class MakeSuperUserViewSet(generics.RetrieveUpdateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = SuperUserSerializer(partial=True)
    lookup_field = "username"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.name = request.data.get("name")
        # instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)