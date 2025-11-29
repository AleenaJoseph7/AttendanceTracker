from django.shortcuts import render, redirect
from TeacherApp.models import Studentdb, Internalmarkdb, ChatMessage, Attendancedb, Subjectdb


# Create your views here.
def StudentHomePage(request):
    return render(request, "base.html")


def StudentLoginPage(request):
    return render(request, "StudentLoginPage.html")


def StudentLogin(request):
    if request.method == 'POST':
        regid = request.POST.get('regid')
        password = request.POST.get('password')

        if Studentdb.objects.filter(Student_regid=regid, Student_password=password).exists():
            return redirect(StudentHomePage)
        else:
            return redirect(StudentLoginPage)
