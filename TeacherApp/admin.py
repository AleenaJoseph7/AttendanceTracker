from django.contrib import admin
from TeacherApp.models import Studentdb,Subjectdb,Attendancedb,Internalmarkdb

# Register your models here.
admin.site.register(Subjectdb)
admin.site.register(Studentdb)
admin.site.register(Internalmarkdb)
admin.site.register(Attendancedb)