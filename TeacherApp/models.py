from django.db import models

# Create your models here.
class Studentdb(models.Model):
    Student_name=models.CharField(max_length=30,null=True,blank=True)
    Student_rollno=models.IntegerField(null=True,blank=True)
    Student_regid=models.CharField(max_length=30,null=True,blank=True)
    Student_batch=models.CharField(max_length=30,null=True,blank=True)
    Student_sem=models.CharField(max_length=30,null=True,blank=True)
    Student_duration=models.CharField(max_length=30,null=True,blank=True)
    Student_prof=models.ImageField(upload_to="Student Profile Image",null=True,blank=True)