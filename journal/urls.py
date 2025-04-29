from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JournalViewSet, RegisterView

router = DefaultRouter()
router.register(r'journals', JournalViewSet, basename='journal')

urlpatterns = [
    path('', include(router.urls)),
    path('users/register/', RegisterView.as_view(), name='register'),
]