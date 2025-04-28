from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Journal
from .serializers import JournalSerializer
from .utils import analyze_sentiment


class JournalViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer

    def get_queryset(self):
        # Only return journals belonging to the authenticated user
        return Journal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # If mood is not provided, analyze the sentiment using DeepSeek
        content = serializer.validated_data.get('content')
        mood = serializer.validated_data.get('mood')

        if not mood:  # If mood is not provided by the user
            mood = analyze_sentiment(content)

        # Save the journal with the determined mood
        serializer.save(user=self.request.user, mood=mood)
