from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
from  django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
import datetime
from datetime import date

from TeacherApp.models import Studentdb,Subjectdb,Attendancedb,Internalmarkdb


# Create your views here.
def Indexpage(request):
    date=datetime.datetime.now()
    student_count=Studentdb.objects.count()
    subject_count=Subjectdb.objects.count()
    return render(request,"index.html",{'student_count':student_count,'subject_count':subject_count,'date':date})

def Addstudentpage(request):
    date = datetime.datetime.now()
    return render(request,'addstudent.html',{'date':date})

def savestudent(request):
    if request.method=='POST':
        student_name=request.POST.get('student_name')
        student_rollno=request.POST.get('student_rollno')
        student_regid=request.POST.get('student_regid')
        student_batch=request.POST.get('student_batch')
        student_sem=request.POST.get('student_sem')
        student_duration=request.POST.get('student_duration')
        student_phone = request.POST.get('student_phone')
        student_prof=request.FILES.get('student_prof')


        ob=Studentdb(Student_name=student_name,
                     Student_rollno=student_rollno,
                     Student_regid=student_regid,
                     Student_batch=student_batch,
                     Student_sem=student_sem,
                     Student_duration=student_duration,
                     Student_phone=student_phone,
                     Student_prof=student_prof)

        ob.save()
        return redirect(Addstudentpage)

def DisplaystudentPage(request):
    date = datetime.datetime.now()
    data=Studentdb.objects.all()
    return render(request,"displaystudent.html",{'data':data,'date':date})


def EditstudentPage(request,s_id):
    date = datetime.datetime.now()
    student=Studentdb.objects.get(id=s_id)
    return render(request,"editstudent.html",{'student':student,'date':date})

def updatestudent(request,s_id):
    if request.method=='POST':
        student_name=request.POST.get('student_name')
        student_rollno=request.POST.get('student_rollno')
        student_regid=request.POST.get('student_regid')
        student_batch=request.POST.get('student_batch')
        student_sem=request.POST.get('student_sem')
        student_duration=request.POST.get('student_duration')
        student_phone = request.POST.get('student_phone')
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
                     Student_phone=student_phone,
                     Student_prof=files)

        return redirect(DisplaystudentPage)

def deletestudent(request,s_id):
    data=Studentdb.objects.filter(id=s_id)
    data.delete()
    return redirect(DisplaystudentPage)


def AddsubjectPage(request):
    date = datetime.datetime.now()
    return render(request,"addsubject.html",{'date':date})

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
    date = datetime.datetime.now()
    data=Subjectdb.objects.all()
    return render(request,"displaysubject.html",{'data':data,'date':date})

def EditsubjectPage(request,sub_id):
    date = datetime.datetime.now()
    subject=Subjectdb.objects.get(id=sub_id)
    return render(request,"editsubject.html",{'subject':subject,'date':date})

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

def Addinternalpage(request):
    date = datetime.datetime.now()
    student=Studentdb.objects.all()
    subject=Subjectdb.objects.all()
    return render(request,"addinternal.html",{'student':student,'subject':subject,'date':date})

def Saveinternal(request):
    if request.method=='POST':
        student_id=request.POST.get('student')
        subject_id=request.POST.get('subject')
        internalmark=request.POST.get('internalmark')
        totalmark=request.POST.get('totalmark')

        student=Studentdb.objects.get(id=student_id)
        subject=Subjectdb.objects.get(id=subject_id)

        ob=Internalmarkdb(Student=student,
                          Subject=subject,
                          Internalmark=internalmark,
                          Totalmark=totalmark)
        ob.save()
        return redirect(Addinternalpage)
def Displayinternal(request):
    date = datetime.datetime.now()
    data=Internalmarkdb.objects.all()
    return render(request,"displayinternal.html",{'data':data,'date':date})

def Editinternalpage(request,i_id):
    date = datetime.datetime.now()
    student = Studentdb.objects.all()
    subject = Subjectdb.objects.all()
    internal=Internalmarkdb.objects.get(id=i_id)
    return render(request,"editinternal.html",{'student':student,'subject':subject,'internal':internal,'date':date})


def Updateinternal(request,i_id):
    if request.method=='POST':
        student_id=request.POST.get('student')
        subject_id=request.POST.get('subject')
        internalmark=request.POST.get('internalmark')
        totalmark=request.POST.get('totalmark')

        student = Studentdb.objects.get(id=student_id)
        subject = Subjectdb.objects.get(id=subject_id)

        Internalmarkdb.objects.filter(id=i_id).update(Student=student,
                          Subject=subject,
                          Internalmark=internalmark,
                          Totalmark=totalmark)
        return redirect(Displayinternal)

def Deleteinternal(request,i_id):
    data=Internalmarkdb.objects.filter(id=i_id)
    data.delete()
    return redirect(Displayinternal)

def AttendancePage(request):
    subject=Subjectdb.objects.all()
    student=Studentdb.objects.all()
    date=datetime.datetime.now()
    return render(request,"addattendance.html",{'date':date,'subject':subject,'student':student})

def saveattendance(request):
    if request.method=='POST':
        attendance_student=request.POST.get('attendance_student')
        attendance_subject=request.POST.get('attendance_subject')
        attendance_date=request.POST.get('attendance_date')
        attendance_status=request.POST.get('attendance_status')

        attendance_studentobj=Studentdb.objects.get(id=attendance_student)
        attendance_subjectobj=Subjectdb.objects.get(id=attendance_subject)

        ob=Attendancedb(Student=attendance_studentobj,
                        Subject=attendance_subjectobj,
                        Date=attendance_date,
                        Status=attendance_status)

        ob.save()
        return redirect(AttendancePage)

def Displayattendancepage(request):
    date = datetime.datetime.now()
    data=Attendancedb.objects.all()
    return render(request,"displayattendance.html",{'date':date,'data':data})

def Editattendancepage(request,a_id):
    subject = Subjectdb.objects.all()
    student = Studentdb.objects.all()
    date = datetime.datetime.now()
    attendance=Attendancedb.objects.get(id=a_id)
    return render(request,"editattendance.html", {'date': date,'attendance':attendance,'subject':subject,'student':student})

def updateattendance(request,a_id):
    if request.method == 'POST':
        attendance_student = request.POST.get('attendance_student')
        attendance_subject = request.POST.get('attendance_subject')
        attendance_date = request.POST.get('attendance_date')
        attendance_status = request.POST.get('attendance_status')

        attendance_studentobj = Studentdb.objects.get(id=attendance_student)
        attendance_subjectobj = Subjectdb.objects.get(id=attendance_subject)

        Attendancedb.objects.filter(id=a_id).update(Student=attendance_studentobj,
                          Subject=attendance_subjectobj,
                          Date=attendance_date,
                          Status=attendance_status)
        return redirect(Displayattendancepage)

def deleteattendance(request,a_id):
    data=Attendancedb.objects.filter(id=a_id)
    data.delete()
    return redirect(Displayattendancepage)







def AdminLoginPage(request):
    return render(request,"adminlogin.html")

def AdminLogin(request):
    if request.method=='POST':
        admin_username=request.POST.get('admin_username')
        admin_password=request.POST.get('admin_password')

        if User.objects.filter(username__contains=admin_username).exists():
            data=authenticate(username=admin_username,password=admin_password)

            if data is not None:
                login(request,data)
                request.session['Username']=admin_username
                request.session['Password']=admin_password
                return redirect(Indexpage)

            else:
                return redirect(AdminLoginPage)
        else:
            return redirect(AdminLoginPage)

def AdminLogout(request):
    del request.session['Username']
    del request.session['Password']
    return redirect(AdminLoginPage)



