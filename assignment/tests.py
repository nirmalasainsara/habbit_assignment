from django.test import TestCase
import json
from django.contrib.auth.models import User
from .models import Course
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .serializers import RegisterSerializer, CourseSerializer
from datetime import datetime, timezone
import datetime
import pytz


class RegistrationTestcase(APITestCase):
    def test_registration(self):
        data = {
            "username": "veerkumar",
            "password": "veer@123",
            "email": "veer@gmail.com",
        }
        response = self.client.post("http://127.0.0.1:8000/habbit/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourseTestcase(APITestCase):
    def test_course(self):
        data = {
            "name": "Book",
            "author": "chetan bagat",
            "date": datetime.datetime(2021, 6, 16, 10, 24, 0, 0, pytz.UTC),
            "price": 90,
        }
        response = self.client.post("http://127.0.0.1:8000/habbit/add_course/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
