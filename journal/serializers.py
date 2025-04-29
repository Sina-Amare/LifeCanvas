from rest_framework import serializers
from .models import Journal
from django.contrib.auth import get_user_model

User = get_user_model()

class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Journal
        fields = ['id', 'title', 'content', 'mood',
                  'location', 'labels', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'mood']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        # Check email format (additional validation)
        email = data['email']
        if "@" not in email or "." not in email:
            raise serializers.ValidationError({"error": "Please enter a valid email address."})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "This email is already registered."})

        # Check if username already exists
        username = data['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error": "This username is already taken."})

        # Check username format (optional: only allow alphanumeric and underscores)
        if not username.replace('_', '').isalnum():
            raise serializers.ValidationError({"error": "Username can only contain letters, numbers, and underscores."})

        return data

    def create(self, validated_data):
        # Remove confirm_password from validated data as it's not needed for user creation
        validated_data.pop('confirm_password')
        # Create user with hashed password
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user