from django.db import models

# Create your models here.
class Login(models.Model):
    uname=models.CharField(max_length=50)
    pwd=models.CharField(max_length=50)
    role=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
class Registration(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=50)
    hname=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    zipcode=models.BigIntegerField()
    email=models.CharField(max_length=50)
    phno=models.BigIntegerField()
    uname=models.CharField(max_length=50)