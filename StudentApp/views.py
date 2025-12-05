from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from TeacherApp.models import Studentdb, Internalmarkdb, ChatMessage, Attendancedb, Subjectdb
from django.contrib import messages


# Create your views here.
def StudentHomePage(request):
    student=Studentdb.objects.filter(Student_name=request.session['Username']).first()
    return render(request, "base.html",{'student':student})


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
            messages.success(request, "Login Successfully!")
            return redirect(StudentHomePage)
        else:
            messages.warning(request, "Username or Password!")
            return redirect(StudentLoginPage)


def StudentLogout(request):
    del request.session['Username']
    del request.session['Password']
    messages.success(request, "Logout Successfully!")
    return redirect(StudentLoginPage)
