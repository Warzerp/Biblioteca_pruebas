from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegistroSerializer, PerfilSerializer, CustomUserSerializer
from .permissions import EsBibliotecario

User = get_user_model()


class RegistroView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistroSerializer


class PerfilView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PerfilSerializer

    def get_object(self):
        return self.request.user


class UsuarioListView(generics.ListAPIView):
    permission_classes = [EsBibliotecario]
    serializer_class = CustomUserSerializer
    queryset = User.objects.all().order_by('username')
