from rest_framework import serializers
from .models import Course, Forgotpassword
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User = get_user_model()

# course serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


# register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "email")

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            return email
        else:
            raise serializers.ValidationError("Email does not valid")


class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=15)
    password2 = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=15)
    user = serializers.CharField(max_length=15)

    def validate(self, data):
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 == password2:
            return data
        raise serializers.ValidationError("password does not valid")
