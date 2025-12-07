from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from TeacherApp.models import Studentdb, Internalmarkdb, ChatMessage, Attendancedb, Subjectdb
from django.contrib import messages


# Create your views here.
def StudentHomePage(request):
    student=Studentdb.objects.get(id=request.session['StudentId'])
    if not student:
        messages.error(request,"please Login !")
        return redirect(StudentLoginPage)
    return render(request, "base.html",{'student':student})

def StudentReportPage(request):
    student=Studentdb.objects.get(id=request.session['StudentId'])
    internal=Internalmarkdb.objects.filter(Student=request.session['StudentId'])

    attendance=[]

    for i in internal:
        subject=i.Subject
        Total_class=Attendancedb.objects.filter(Student=student,Subject=subject).count()
        present_class=Attendancedb.objects.filter(Student=student,Subject=subject,Status="Present").count()
        if Total_class==0:
            percentages=0
        else:
            percentages=round((present_class/Total_class)*100)
        attendance.append({'subject':subject,
                           'subjectcode':subject.Subject_code,
                           'internalmark':i.Internalmark,
                           'totalmark':i.Totalmark,
                           'percentages':percentages})

    return render(request,'StudentReport.html',{'student':student,'internal':internal,'attendance':attendance})


def StudentLoginPage(request):
    return render(request, "StudentLoginPage.html")


def StudentLogin(request):
    if request.method == 'POST':
        regid = request.POST.get('regid')
        password = request.POST.get('password')

        if Studentdb.objects.filter(Student_regid=regid, Student_password=password).exists():
            student = Studentdb.objects.get(Student_regid=regid)
            request.session['StudentId'] = student.id
            messages.success(request, "Login Successfully!")
            return redirect(StudentHomePage)
        else:
            messages.warning(request, "Username or Password!")
            return redirect(StudentLoginPage)


def StudentLogout(request):
    del request.session['StudentId']
    messages.success(request, "Logout Successfully!")
    return redirect(StudentLoginPage)
