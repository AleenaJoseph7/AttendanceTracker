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
            student = Studentdb.objects.get(Student_regid=regid)
            request.session['Username'] = student.Student_name
            request.session['Password'] = password
            return redirect(StudentHomePage)
        else:
            return redirect(StudentLoginPage)


def StudentLogout(request):
    del request.session['Username']
    del request.session['Password']
    return render(StudentLoginPage)
