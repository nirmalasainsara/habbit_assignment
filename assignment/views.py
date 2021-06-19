from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.views import APIView
from .models import Course, Forgotpassword
from .serializers import (
    CourseSerializer,
    RegisterSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
import random
from django.contrib.auth.models import User


# Create course view
class CourseView(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# course detail view where the user can  edit and delete the course.
class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    lookup_url_kwarg = "id"
    queryset = Course.objects.all()


# User register view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            register = serializer.save()
            serializer = RegisterSerializer(register)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# forgot password
class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            code = random.randrange(10000000, 999999999)
            email = serializer.validated_data.get("email")
            user = User.objects.get(email=email)
            send_mail(
                "reset password",
                f"to change your password follow this link:http://127.0.0.1:8000/habbit/reset_password/?code={code}&user={user.id}",
                "nirmlasainsara909@gmail.com",
                ["nirmlasainsara909@gmail.com"],
                fail_silently=False,
            )

            Forgotpassword.objects.create(user=user, code=code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# password reset view
class ResetPasswordView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        code = self.query_params.get("code")
        user_id = self.query_params.get("user")
        qs = Forgotpassword.objects.filter(code=code, user_id=user_id)
        if qs.exists():
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get("code")
            user_id = serializer.validated_data.get("user")

            qs = Forgotpassword.objects.filter(code=code, user_id=user_id)
            if qs.exists():
                password1 = serializer.validated_data.get("password1")
                user = User.objects.get(id=user_id)
                user.set_password(password1)
                user.save()
                qs.delete()
                return Response(
                    {"message": "Your password is change successfully"},
                    status=status.HTTP_201_CREATED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
