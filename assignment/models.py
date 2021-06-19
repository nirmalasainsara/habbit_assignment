from django.db import models
from django.contrib.auth.models import User

# course model
class Course(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    date = models.DateTimeField()
    price = models.IntegerField()


class Forgotpassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=200)
