from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from  django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

from TeacherApp.models import Studentdb,Subjectdb


# Create your views here.
def Indexpage(request):
    student_count=Studentdb.objects.count()
    subject_count=Subjectdb.objects.count()
    return render(request,"index.html",{'student_count':student_count,'subject_count':subject_count})

def Addstudentpage(request):
    return render(request,'addstudent.html')

def savestudent(request):
    if request.method=='POST':
        student_name=request.POST.get('student_name')
        student_rollno=request.POST.get('student_rollno')
        student_regid=request.POST.get('student_regid')
        student_batch=request.POST.get('student_batch')
        student_sem=request.POST.get('student_sem')
        student_duration=request.POST.get('student_duration')
        student_prof=request.FILES.get('student_prof')

        ob=Studentdb(Student_name=student_name,
                     Student_rollno=student_rollno,
                     Student_regid=student_regid,
                     Student_batch=student_batch,
                     Student_sem=student_sem,
                     Student_duration=student_duration,
                     Student_prof=student_prof)

        ob.save()
        return redirect(Addstudentpage)

def DisplaystudentPage(request):
    data=Studentdb.objects.all()
    return render(request,"displaystudent.html",{'data':data})


def EditstudentPage(request,s_id):
    student=Studentdb.objects.get(id=s_id)
    return render(request,"editstudent.html",{'student':student})

def updatestudent(request,s_id):
    if request.method=='POST':
        student_name=request.POST.get('student_name')
        student_rollno=request.POST.get('student_rollno')
        student_regid=request.POST.get('student_regid')
        student_batch=request.POST.get('student_batch')
        student_sem=request.POST.get('student_sem')
        student_duration=request.POST.get('student_duration')
        try:
            student_prof=request.FILES['student_prof']
            fs=FileSystemStorage()
            files=fs.save(student_prof.name,student_prof)

        except MultiValueDictKeyError:
            files=Studentdb.objects.get(id=s_id).Student_prof

        Studentdb.objects.filter(id=s_id).update(Student_name=student_name,
                     Student_rollno=student_rollno,
                     Student_regid=student_regid,
                     Student_batch=student_batch,
                     Student_sem=student_sem,
                     Student_duration=student_duration,
                     Student_prof=files)

        return redirect(DisplaystudentPage)

def deletestudent(request,s_id):
    data=Studentdb.objects.filter(id=s_id)
    data.delete()
    return redirect(DisplaystudentPage)


def AddsubjectPage(request):
    return render(request,"addsubject.html")

def savesubject(request):
    if request.method=='POST':
        subject_name=request.POST.get('subject_name')
        subject_code=request.POST.get('subject_code')
        subject_teacher=request.POST.get('subject_teacher')
        subject_sem=request.POST.get('subject_sem')
        subject_dep=request.POST.get('subject_dep')

        ob=Subjectdb(Subject_name=subject_name,
                     Subject_code= subject_code,
                     Subject_teacher=subject_teacher,
                     Subject_sem=subject_sem,
                     Subject_dep=subject_dep)

        ob.save()
        return redirect(AddsubjectPage)

def DisplaysubjectPage(request):
    data=Subjectdb.objects.all()
    return render(request,"displaysubject.html",{'data':data})

def EditsubjectPage(request,sub_id):
    subject=Subjectdb.objects.get(id=sub_id)
    return render(request,"editsubject.html",{'subject':subject})

def Updatesubject(request,sub_id):
    if request.method=='POST':
        subject_name=request.POST.get('subject_name')
        subject_code=request.POST.get('subject_code')
        subject_teacher=request.POST.get('subject_teacher')
        subject_sem=request.POST.get('subject_sem')
        subject_dep=request.POST.get('subject_dep')

        Subjectdb.objects.filter(id=sub_id).update(Subject_name=subject_name,
                     Subject_code= subject_code,
                     Subject_teacher=subject_teacher,
                     Subject_sem=subject_sem,
                     Subject_dep=subject_dep)

        return redirect(DisplaysubjectPage)

def Deletesubject(request,sub_id):
    data=Subjectdb.objects.filter(id=sub_id)
    data.delete()
    return redirect(DisplaysubjectPage)




