from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Journal
from .serializers import JournalSerializer


class JournalViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer

    def get_queryset(self):
        # Only return journals belonging to the authenticated user
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)
