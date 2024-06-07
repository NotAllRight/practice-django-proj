from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model, hashers

from .serializers import CustomUserSerializer


User = get_user_model()

class CustomUserViewSet(viewsets.ModelViewSet):
    """Клас вiдображення моделi CustomUser"""

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    # Хешування паролю при створеннi користувача
    def perform_create(self, serializer):
        password = self.request.data.get('password')
        hashed_password = hashers.make_password(password)
        serializer.save(password=hashed_password)