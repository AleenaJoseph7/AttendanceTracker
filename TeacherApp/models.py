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

class Subjectdb(models.Model):
    Subject_name=models.CharField(max_length=30,null=True,blank=True)
    Subject_code=models.CharField(max_length=30,null=True,blank=True)
    Subject_teacher=models.CharField(max_length=30,null=True,blank=True)
    Subject_sem=models.CharField(max_length=30,null=True,blank=True)
    Subject_dep=models.CharField(max_length=30,null=True,blank=True)