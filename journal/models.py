from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Journal(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('angry', 'Angry'),
        ('neutral', 'Neutral'),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='journals')
    title = models.CharField(max_length=200)
    content = models.TextField()
    mood = models.CharField(
        max_length=50, choices=MOOD_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.email}"
