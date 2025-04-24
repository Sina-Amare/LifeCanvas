from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import serializers


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token (optional)
        token['email'] = user.email
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # Map email to username for authentication
        email = attrs.get('email')
        password = attrs.get('password')

        # Find user by email
        user = self.get_user(email=email)
        if user and user.check_password(password):
            # If user exists and password is correct, proceed with token generation
            data = super().validate(attrs)
            data['email'] = user.email
            data['username'] = user.username
            return data
        else:
            raise serializers.ValidationError('Invalid email or password')

    def get_user(self, email):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
