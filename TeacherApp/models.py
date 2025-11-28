from django.db import models

from datetime import date


# Create your models here.
class Studentdb(models.Model):
    Student_name = models.CharField(max_length=30, null=True, blank=True)
    Student_rollno = models.IntegerField(null=True, blank=True)
    Student_regid = models.CharField(max_length=30, null=True, blank=True)
    Student_batch = models.CharField(max_length=30, null=True, blank=True)
    Student_sem = models.CharField(max_length=30, null=True, blank=True)
    Student_duration = models.CharField(max_length=30, null=True, blank=True)
    Student_phone = models.IntegerField(null=True, blank=True)
    Student_prof = models.ImageField(upload_to="Student Profile Image", null=True, blank=True)
    Student_password = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.Student_name


class Subjectdb(models.Model):
    Subject_name = models.CharField(max_length=30, null=True, blank=True)
    Subject_code = models.CharField(max_length=30, null=True, blank=True)
    Subject_teacher = models.CharField(max_length=30, null=True, blank=True)
    Subject_sem = models.CharField(max_length=30, null=True, blank=True)
    Subject_dep = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.Subject_code


class Attendancedb(models.Model):
    Student = models.ForeignKey(Studentdb, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subjectdb, on_delete=models.CASCADE)
    Date = models.DateField(default=date.today)
    Status = models.CharField(max_length=10, default="Absent", choices=[("Present", "Present"),
                                                                        ("Absent", "Absent")])

# ("Present", "Present") 1st data to be stored to db, 2nd visible to user

    def __str__(self):
        return f"{self.Student.Student_name} - {self.Subject.Subject_code} - {self.Date}"


class Internalmarkdb(models.Model):
    Student = models.ForeignKey(Studentdb, on_delete=models.CASCADE)
    Subject = models.ForeignKey(Subjectdb, on_delete=models.CASCADE)
    Internalmark = models.IntegerField(null=False, blank=False)
    Totalmark = models.IntegerField(null=False, blank=False, default=50)

    def __str__(self):
        return f"{self.Student.Student_name} - {self.Subject.Subject_name}"


class ChatMessage(models.Model):
    sender = models.CharField(max_length=20)
    student = models.ForeignKey(Studentdb, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.CharField(
        max_length=10,
        default="sent",
        choices=[
            ("sent", "Sent"),
            ("delivered", "Delivered"),
            ("read", "Read"),
        ]
    )

    class Meta:
        ordering = ['timestamp']
