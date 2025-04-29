from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter
from .models import Journal
from .serializers import JournalSerializer, UserRegistrationSerializer
from .utils import analyze_sentiment

# Custom FilterSet to handle JSONField filtering for 'labels'
class JournalFilter(FilterSet):
    labels = CharFilter(method='filter_labels')  # Custom filter for JSONField

    class Meta:
        model = Journal
        fields = ['created_at', 'location', 'labels']

    def filter_labels(self, queryset, name, value):
        # Filter journals where the labels array contains the given value
        return queryset.filter(labels__contains=[value])

class JournalViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = JournalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = JournalFilter  # Use the custom FilterSet instead of filterset_fields

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

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT token for the new user
            token = AccessToken.for_user(user)
            return Response({
                'access': str(token),
                'user': {'email': user.email, 'username': user.username}
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)