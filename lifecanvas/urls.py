from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView
from users.jwt_views import CustomTokenObtainPairView
from django.contrib import admin


class TestAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": "DRF is working!",
            "user": {
                "email": request.user.email,
                "username": request.user.username
            }
        })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', TestAPIView.as_view(), name='test-api'),
    path('api/users/', include('users.urls')),
    path('api/journal/', include('journal.urls')),  # Add journal app URLs
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
