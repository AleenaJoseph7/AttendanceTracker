from django.db import models

# Create your models here.
class Studentdb(models.Model):
    Student_name=models.CharField(max_length=30,null=True,blank=True)
    Student_rollno=models.IntegerField(null=True,blank=True)
    Student_regid=models.CharField(max_length=30,null=True,blank=True)
    Student_batch=models.CharField(max_length=30,null=True,blank=True)
    Student_sem=models.CharField(max_length=30,null=True,blank=True)
    Student_duration=models.CharField(max_length=30,null=True,blank=True)
    Student_phone = models.IntegerField(null=True, blank=True)
    Student_prof=models.ImageField(upload_to="Student Profile Image",null=True,blank=True)

    def __str__(self):
        return self.Student_name

class Subjectdb(models.Model):
    Subject_name=models.CharField(max_length=30,null=True,blank=True)
    Subject_code=models.CharField(max_length=30,null=True,blank=True)
    Subject_teacher=models.CharField(max_length=30,null=True,blank=True)
    Subject_sem=models.CharField(max_length=30,null=True,blank=True)
    Subject_dep=models.CharField(max_length=30,null=True,blank=True)

    def __str__(self):
        return self.Subject_code


class Attendancedb(models.Model):
    Student=models.ForeignKey(Studentdb,on_delete=models.CASCADE)
    Subject=models.ForeignKey(Subjectdb,on_delete=models.CASCADE)
    Date=models.DateField(auto_now_add=True)
    Status=models.CharField(max_length=10,default="Absent",choices=[("Present","Present"),
                                                                    ("Absent","Absent")])
    # ("Present", "Present") 1st data to be stored to db, 2nd visible to user
    def __str__(self):
        return self.Student