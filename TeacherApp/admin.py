from django.contrib import admin
from TeacherApp.models import Studentdb,Subjectdb,Attendancedb,Internalmarkdb,ChatMessage

# Register your models here.
admin.site.register(Subjectdb)
admin.site.register(Studentdb)
admin.site.register(Internalmarkdb)
admin.site.register(Attendancedb)
admin.site.register(ChatMessage)