from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    gender = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=10)
    email=models.EmailField()

    def __str__(self):
        return self.user.username

class Institute(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    Institute_Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    Institute_Number = models.CharField(max_length=100)
    ContactNo = models.CharField(max_length=100)
    Website = models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.user.username


