from django.contrib import admin
from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response


class TestAPIView(APIView):
    def get(self, request):
        return Response({"message": "DRF is working!"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test/', TestAPIView.as_view(), name='test-api'),
]
