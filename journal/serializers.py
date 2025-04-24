from rest_framework import serializers
from .models import Journal


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'title', 'content', 'mood', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
