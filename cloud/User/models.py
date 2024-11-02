from django.db import models
# Create your models here.
class file(models.Model):
    fname=models.FileField(upload_to="file")
    uname=models.CharField(max_length=50)
    status=models.CharField(max_length=10)
class encrypt(models.Model):
    uname=models.CharField(max_length=50)
    key=models.CharField(max_length=500)
    fid=models.IntegerField ()
    status=models.CharField(max_length=50)
class blockaes(models.Model):
    encrypt=models.IntegerField()
    block=models.TextField()
class blockdes(models.Model):
    encrypt=models.IntegerField()
    block=models.TextField()
class blockrc2(models.Model):
    encrypt=models.IntegerField()
    block=models.TextField()
class payment1(models.Model):
    fid=models.IntegerField()
    amt=models.BigIntegerField()


