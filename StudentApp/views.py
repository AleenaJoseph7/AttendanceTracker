from django.shortcuts import render,redirect
from TeacherApp.models import Studentdb,Internalmarkdb,ChatMessage,Attendancedb,Subjectdb


# Create your views here.
def StudentHomePage(request):
    return render(request,"base.html")

def StudentLoginPage(request):
    return render(request,"StudentLoginPage.html")

def StudentLogin(request):
    if request.method=='POST':
