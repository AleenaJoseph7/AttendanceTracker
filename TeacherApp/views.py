from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import datetime
from datetime import date
from django.db.models import Count, Q

from django.http import FileResponse
from .utils.pdf_generator import generate_pdf_table
from reportlab.lib import colors

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from TeacherApp.models import Studentdb, Subjectdb, Attendancedb, Internalmarkdb, ChatMessage

from django.contrib import messages
from django.utils.timezone import localtime

import re


# Create your views here.
def Indexpage(request):
    date = datetime.datetime.now()
    student_count = Studentdb.objects.count()
    subject_count = Subjectdb.objects.count()
    today = datetime.date.today()
    attendance_today = Attendancedb.objects.filter(Date=today)

    total_class = attendance_today.count()
    present_count = attendance_today.filter(Status="Present").count()

    if total_class > 0:
        today_percentage = round((present_count / total_class) * 100, 2)
    else:
        today_percentage = 0
    return render(request, "index.html", {'student_count': student_count, 'subject_count': subject_count, 'date': date,
                                          'today_percentage': today_percentage, })


def Addstudentpage(request):
    date = datetime.datetime.now()
    return render(request, 'addstudent.html', {'date': date})


def savestudent(request):
    if request.method == 'POST':

        student_name = request.POST.get('student_name')
        student_rollno = request.POST.get('student_rollno')
        student_regid = request.POST.get('student_regid')
        student_batch = request.POST.get('student_batch')
        student_sem = request.POST.get('student_sem')
        student_duration = request.POST.get('student_duration')
        student_phone = request.POST.get('student_phone')
        student_email = request.POST.get('student_email')
        student_password = request.POST.get('student_password')
        student_confirm = request.POST.get('student_confirm')
        student_prof = request.FILES.get('student_prof')

        name_regex = r'^[A-Z][A-Za-z]*(?:\s(?:[A-Z][A-Za-z]*|[A-Z](?:\.[A-Z])+))+$'
        roll_regex = r'^(?:[1-9][0-9]?|100)$'
        reg_regex = r'^[A-Z0-9]+$'
        duration_regex = r'^\d{4}-\d{4}$'
        phone_regex = r'^[6-9]\d{9}$'
        gmail_regex = r'^[a-z0-9._]+@gmail\.com$'
        pwd_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#]).{6,}$'

        if not re.match(name_regex, student_name):
            messages.error(request, "Name must contain only alphabets, space and dot")
            return redirect(Addstudentpage)

        if not re.match(roll_regex, student_rollno):
            messages.error(request, "Roll number must be from 1")
            return redirect(Addstudentpage)

        if not re.match(reg_regex, student_regid):
            messages.error(request, "Register ID must be CAPITAL letters and numbers only")
            return redirect(Addstudentpage)

        if not student_batch:
            messages.error(request, "Please select a batch")
            return redirect(Addstudentpage)

        if not student_sem:
            messages.error(request, "Please select a semester")
            return redirect(Addstudentpage)

        if not re.match(duration_regex, student_duration):
            messages.error(request, "Duration must be in YYYY-YYYY format")
            return redirect(Addstudentpage)

        if not re.match(phone_regex, student_phone):
            messages.error(request, "Enter a valid 10-digit  mobile number")
            return redirect(Addstudentpage)

        if not re.match(gmail_regex, student_email):
            messages.error(request, "Only Gmail (@gmail.com) email IDs are allowed")
            return redirect(Addstudentpage)

        if not re.match(pwd_regex, student_password):
            messages.error(
                request,
                "Password must contain 1 uppercase, 1 digit, 1 special (@/#) and minimum 6 characters"
            )
            return redirect(Addstudentpage)

        if student_password != student_confirm:
            messages.error(request, "Password and Confirm Password do not match")
            return redirect(Addstudentpage)

        obj = Studentdb(
            Student_name=student_name,
            Student_rollno=student_rollno,
            Student_regid=student_regid,
            Student_batch=student_batch,
            Student_sem=student_sem,
            Student_duration=student_duration,
            Student_phone=student_phone,
            Student_email=student_email,
            Student_password=student_password,
            Student_confirm=student_confirm,
            Student_prof=student_prof
        )
        obj.save()

        messages.success(request, "Student added successfully")
        return redirect(Addstudentpage)


def DisplaystudentPage(request):
    date = datetime.datetime.now()
    data = Studentdb.objects.all()
    return render(request, "displaystudent.html", {'data': data, 'date': date})


def EditstudentPage(request, s_id):
    date = datetime.datetime.now()
    student = Studentdb.objects.get(id=s_id)
    return render(request, "editstudent.html", {'student': student, 'date': date})


def updatestudent(request, s_id):
    if request.method == 'POST':

        student_name = request.POST.get('student_name')
        student_rollno = request.POST.get('student_rollno')
        student_regid = request.POST.get('student_regid')
        student_batch = request.POST.get('student_batch')
        student_sem = request.POST.get('student_sem')
        student_duration = request.POST.get('student_duration')
        student_phone = request.POST.get('student_phone')
        student_email = request.POST.get('student_email')
        student_password = request.POST.get('student_password')
        student_confirm = request.POST.get('student_confirm')
        try:
            student_prof = request.FILES['student_prof']
            fs = FileSystemStorage()
            files = fs.save(student_prof.name, student_prof)
        except MultiValueDictKeyError:
            files = Studentdb.objects.get(id=s_id).Student_prof



        name_regex = r'^[A-Z][A-Za-z]*(?:\s(?:[A-Z][A-Za-z]*|[A-Z](?:\.[A-Z])+))+$'
        roll_regex = r'^(?:[1-9][0-9]?|100)$'
        reg_regex = r'^[A-Z0-9]+$'
        duration_regex = r'^\d{4}-\d{4}$'
        phone_regex = r'^[6-9]\d{9}$'
        gmail_regex = r'^[a-z0-9._]+@gmail\.com$'
        pwd_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#]).{6,}$'

        if not re.match(name_regex, student_name):
            messages.error(request, "Enter a valid Student Name (eg: Anu M.K or Anu Joseph)")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(roll_regex, student_rollno):
            messages.error(request, "Enter a valid Roll Number between 1 and 100")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(reg_regex, student_regid):
            messages.error(request, "Register Number must contain capital letters and digits only")
            return redirect(EditstudentPage,s_id=s_id)

        if not student_batch:
            messages.error(request, "Please select a Batch")
            return redirect(EditstudentPage,s_id=s_id)

        if not student_sem:
            messages.error(request, "Please select a Semester")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(duration_regex, student_duration):
            messages.error(request, "Enter Duration in the format YYYY-YYYY")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(phone_regex, student_phone):
            messages.error(request, "Enter a valid 10-digit Mobile Number")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(gmail_regex, student_email):
            messages.error(request, "Enter a valid Gmail address (example@gmail.com)")
            return redirect(EditstudentPage,s_id=s_id)

        if not re.match(pwd_regex, student_password):
            messages.error(
                request,
                "Password must contain at least 1 uppercase letter, 1 digit, 1 special character (@/#), and minimum 6 characters"
            )
            return redirect(EditstudentPage,s_id=s_id)

        if student_password != student_confirm:
            messages.error(request, "Password and Confirm Password do not match")
            return redirect(Addstudentpage)



        Studentdb.objects.filter(id=s_id).update(
            Student_name=student_name,
            Student_rollno=student_rollno,
            Student_regid=student_regid,
            Student_batch=student_batch,
            Student_sem=student_sem,
            Student_duration=student_duration,
            Student_phone=student_phone,
            Student_email=student_email,
            Student_password=student_password,
            Student_confirm=student_confirm,
            Student_prof=files
        )

        messages.success(request, "Student updated successfully")
        return redirect(DisplaystudentPage)


def deletestudent(request, s_id):
    data = Studentdb.objects.filter(id=s_id)
    data.delete()
    messages.error(request, "Student deleted Succesfully")
    return redirect(DisplaystudentPage)


def AddsubjectPage(request):
    date = datetime.datetime.now()
    return render(request, "addsubject.html", {'date': date})


def savesubject(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        subject_teacher = request.POST.get('subject_teacher')
        subject_sem = request.POST.get('subject_sem')
        subject_dep = request.POST.get('subject_dep')

        subject_name_regex=r"^[A-Z][A-Za-z]*(?:\s[A-Za-z]+)*$"
        subject_code_regex=r"^[A-Z0-9]+$"
        subject_teacher_regex = r"^[A-Z][A-Za-z]*(?:\s(?:[A-Z][A-Za-z]*|[A-Z](?:\.[A-Z])+))+$"

        if not re.match(subject_name_regex,subject_name.strip()):
            messages.error(request,"Enter a Valid Subject Name(eg :OS or Operating System")
            return redirect(AddsubjectPage)

        if not re.match(subject_code_regex,subject_code.strip()):
            messages.error(request,"Enter a Valid Subject Code(eg: CST403")
            return redirect(AddsubjectPage)

        if not re.match(subject_teacher_regex,subject_teacher.strip()):
            messages.error(request,"Enter a Valid Name(eg:Anu M.K or Anu Kimal")
            return redirect(AddsubjectPage)

        if not subject_sem:
            messages.error(request,"Please select a Semester")
            return redirect(AddsubjectPage)

        if not subject_dep:
            messages.error(request,"Please select a Department")
            return redirect(AddsubjectPage)


        ob = Subjectdb(Subject_name=subject_name,
                       Subject_code=subject_code,
                       Subject_teacher=subject_teacher,
                       Subject_sem=subject_sem,
                       Subject_dep=subject_dep)

        ob.save()
        messages.success(request, "Subject added Successfully")
        return redirect(AddsubjectPage)


def DisplaysubjectPage(request):
    date = datetime.datetime.now()
    data = Subjectdb.objects.all()
    return render(request, "displaysubject.html", {'data': data, 'date': date})


def EditsubjectPage(request, sub_id):
    date = datetime.datetime.now()
    subject = Subjectdb.objects.get(id=sub_id)
    return render(request, "editsubject.html", {'subject': subject, 'date': date})


def Updatesubject(request, sub_id):
    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        subject_teacher = request.POST.get('subject_teacher')
        subject_sem = request.POST.get('subject_sem')
        subject_dep = request.POST.get('subject_dep')

        subject_name_regex = r"^[A-Z][A-Za-z]*(?:\s[A-Za-z]+)*$"
        subject_code_regex = r"^[A-Z0-9]+$"
        subject_teacher_regex = r"^[A-Z][A-Za-z]*(?:\s(?:[A-Z][A-Za-z]*|[A-Z](?:\.[A-Z])+))+$"

        if not re.match(subject_name_regex, subject_name.strip()):
            messages.error(request, "Enter a Valid Subject Name(eg :OS or Operating System")
            return redirect(EditsubjectPage,sub_id=sub_id)

        if not re.match(subject_code_regex, subject_code.strip()):
            messages.error(request, "Enter a Valid Subject Code(eg: CST403")
            return redirect(EditsubjectPage,sub_id=sub_id)

        if not re.match(subject_teacher_regex, subject_teacher.strip()):
            messages.error(request, "Enter a Valid Name(eg:Anu M.K or Anu Kimal")
            return redirect(EditsubjectPage,sub_id=sub_id)

        if not subject_sem:
            messages.error(request, "Please select a Semester")
            return redirect(EditsubjectPage,sub_id=sub_id)

        if not subject_dep:
            messages.error(request, "Please select a Department")
            return redirect(EditsubjectPage,sub_id=sub_id)

        Subjectdb.objects.filter(id=sub_id).update(Subject_name=subject_name,
                                                   Subject_code=subject_code,
                                                   Subject_teacher=subject_teacher,
                                                   Subject_sem=subject_sem,
                                                   Subject_dep=subject_dep)
        messages.success(request, "Subject updated Succesfully")
        return redirect(DisplaysubjectPage)


def Deletesubject(request, sub_id):
    data = Subjectdb.objects.filter(id=sub_id)
    data.delete()
    messages.success(request, "Subject deleted Successfully")
    return redirect(DisplaysubjectPage)


def Addinternalpage(request):
    date = datetime.datetime.now()
    student = Studentdb.objects.all()
    subject = Subjectdb.objects.all()
    return render(request, "addinternal.html", {'student': student, 'subject': subject, 'date': date})


def Saveinternal(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        internalmark = request.POST.get('internalmark')
        totalmark = request.POST.get('totalmark')

        student = Studentdb.objects.get(id=student_id)
        subject = Subjectdb.objects.get(id=subject_id)

        ob = Internalmarkdb(Student=student,
                            Subject=subject,
                            Internalmark=internalmark,
                            Totalmark=totalmark)
        ob.save()
        messages.success(request, "Internal added Successfully")
        return redirect(Addinternalpage)


def Displayinternal(request):
    import datetime
    date = datetime.datetime.now()
    selected_subject = request.GET.get("subject")  # Subject filter

    data = Internalmarkdb.objects.all()
    if selected_subject:
        data = data.filter(Subject_id=selected_subject)
    subjects = Subjectdb.objects.all()

    return render(
        request,
        "displayinternal.html",
        {
            "data": data,
            "date": date,
            "subjects": subjects,
            "selected_subject": selected_subject,
        }
    )


def Editinternalpage(request, i_id):
    date = datetime.datetime.now()
    student = Studentdb.objects.all()
    subject = Subjectdb.objects.all()
    internal = Internalmarkdb.objects.get(id=i_id)
    return render(request, "editinternal.html",
                  {'student': student, 'subject': subject, 'internal': internal, 'date': date})


def Updateinternal(request, i_id):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        internalmark = request.POST.get('internalmark')
        totalmark = request.POST.get('totalmark')

        student = Studentdb.objects.get(id=student_id)
        subject = Subjectdb.objects.get(id=subject_id)

        Internalmarkdb.objects.filter(id=i_id).update(Student=student,
                                                      Subject=subject,
                                                      Internalmark=internalmark,
                                                      Totalmark=totalmark)
        messages.success(request, "Internal updated Successfully")
        return redirect(Displayinternal)


def Deleteinternal(request, i_id):
    data = Internalmarkdb.objects.filter(id=i_id)
    data.delete()
    messages.success(request, "Internal deleted Successfully")
    return redirect(Displayinternal)


def AttendancePage(request):
    date = datetime.datetime.now()
    subjects = Subjectdb.objects.all()
    subject_id = request.GET.get("subject")
    selected_date = request.GET.get("date")

    if selected_date:
        selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = datetime.date.today()

    sheet = []

    if subject_id:
        subject = Subjectdb.objects.get(id=subject_id)
        students = Studentdb.objects.all()

        for s in students:
            record, created = Attendancedb.objects.get_or_create(
                Student=s,
                Subject=subject,
                Date=selected_date,
                defaults={"Status": "Present"}
            )
            sheet.append(record)

    return render(request, "addattendance.html", {
        "subjects": subjects,
        "sheet": sheet,
        "selected_subject": subject_id,
        "selected_date": selected_date,
        "date": date
    })


def toggle_attendance(request, record_id):
    record = Attendancedb.objects.get(id=record_id)

    if record.Status == "Present":
        record.Status = "Absent"
    else:
        record.Status = "Present"

    record.save()
    return JsonResponse({"status": record.Status})


def saveattendance(request):
    if request.method == 'POST':
        attendance_student = request.POST.get('attendance_student')
        attendance_subject = request.POST.get('attendance_subject')
        attendance_date = request.POST.get('attendance_date')
        attendance_status = request.POST.get('attendance_status')

        attendance_studentobj = Studentdb.objects.get(id=attendance_student)
        attendance_subjectobj = Subjectdb.objects.get(id=attendance_subject)

        ob = Attendancedb(Student=attendance_studentobj,
                          Subject=attendance_subjectobj,
                          Date=attendance_date,
                          Status=attendance_status)

        ob.save()
        messages.success(request, "Attendance added Successfully")
        return redirect(AttendancePage)


def Displayattendancepage(request):
    subject_id = request.GET.get("subject")

    if subject_id:
        data = Attendancedb.objects.filter(Subject_id=subject_id)
    else:
        data = Attendancedb.objects.all()
    date = datetime.datetime.now()
    subjects = Subjectdb.objects.all()
    return render(request, "displayattendance.html",
                  {'date': date, 'data': data, 'subject_id': subject_id, 'subjects': subjects})


def Editattendancepage(request, a_id):
    subject = Subjectdb.objects.all()
    student = Studentdb.objects.all()
    date = datetime.datetime.now()
    attendance = Attendancedb.objects.get(id=a_id)
    return render(request, "editattendance.html",
                  {'date': date, 'attendance': attendance, 'subject': subject, 'student': student})


def updateattendance(request, a_id):
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
        messages.success(request, "Attendance updated Succesfully")
        return redirect(Displayattendancepage)


def deleteattendance(request, a_id):
    data = Attendancedb.objects.filter(id=a_id)
    data.delete()
    messages.success(request, "Attendance deleted Successfully")
    return redirect(Displayattendancepage)


def AttendancePercentagePage(request):
    subjects = Subjectdb.objects.all()
    selected_subject = request.GET.get("subject")
    date = datetime.datetime.now()
    data = []

    if selected_subject:
        data = Attendancedb.objects.filter(Subject_id=selected_subject).values(
            'Student__Student_name',
        ).annotate(
            total=Count('id'),
            present=Count('id', filter=Q(Status="Present")),
            absent=Count('id', filter=Q(Status="Absent"))
        )

        for d in data:
            d['percentage'] = round((d['present'] / d['total']) * 100, 2) if d['total'] else 0

    return render(request, "attendancepercentage.html",
                  {"subjects": subjects, "data": data, "selected_subject": selected_subject, 'date': date})


def internal_pdf(request, subject_id):
    subject = Subjectdb.objects.get(id=subject_id)
    records = Internalmarkdb.objects.filter(Subject=subject)

    data_rows = [["Student Name", "Internal Mark", "Total Mark"]]
    for r in records:
        data_rows.append([r.Student.Student_name, r.Internalmark, r.Totalmark])

    pdf_title = f"{subject.Subject_name}({subject.Subject_code}) Internal Report"
    pdf_buffer = generate_pdf_table(pdf_title, data_rows)

    return FileResponse(pdf_buffer, as_attachment=True, filename="internal_marks.pdf")


def student_attendance_pdf(request, student_id):
    data = Attendancedb.objects.filter(Student_id=student_id).order_by("Date")
    student_name = data[0].Student.Student_name if data else "Student"

    data_rows = [["Student Name", "Date", "Status"]]
    for record in data:
        data_rows.append([record.Student.Student_name, str(record.Date), record.Status])

    column_color_map = {
        2: lambda v: colors.green if v == "Present" else colors.red
    }

    pdf_buffer = generate_pdf_table(f"Attendance Report - {student_name}", data_rows, column_color_map)
    return FileResponse(pdf_buffer, as_attachment=True, filename="student_attendance.pdf")


def subject_attendance_percentage_pdf(request, subject_id):
    subject = Subjectdb.objects.get(id=subject_id)
    data = Attendancedb.objects.filter(Subject_id=subject_id).values(
        'Student__Student_name'
    ).annotate(
        total=Count('id'),
        present=Count('id', filter=Q(Status="Present")),
        absent=Count('id', filter=Q(Status="Absent"))
    )

    for d in data:
        d['percentage'] = round((d['present'] / d['total']) * 100, 2) if d['total'] else 0

    data_rows = [["Student Name", "Total", "Present", "Absent", "Percentage"]]
    for d in data:
        data_rows.append([d['Student__Student_name'], d['total'], d['present'], d['absent'], d['percentage']])

    column_color_map = {4: lambda v: colors.green if float(v) >= 75 else colors.red}

    pdf_buffer = generate_pdf_table(f"{subject.Subject_name}({subject.Subject_code})", data_rows, column_color_map)
    return FileResponse(pdf_buffer, as_attachment=True, filename="attendance_percentage.pdf")


def Chatbotpage(request, student_id):
    students = Studentdb.objects.all()

    unread_map = {
        item["student"]: item["count"]
        for item in ChatMessage.objects.filter(
            sender="student"
        ).exclude(read_status="read")
        .values("student")
        .annotate(count=Count("id"))
    }

    current_student = Studentdb.objects.get(id=student_id)

    context = {
        "students": students,
        "current_student": current_student,
        "unread_map": unread_map,
    }

    return render(request, "Chatbot.html", context)


def MessengerShortcut(request):
    first = Studentdb.objects.order_by("id").first()
    if first:
        return redirect("Chatbotpage", student_id=first.id)
    return redirect("DisplaystudentPage")


def get_messages(request, student_id):
    ChatMessage.objects.filter(
        student_id=student_id,
        sender="student"
    ).exclude(read_status="read").update(read_status="read")

    messages = ChatMessage.objects.filter(student_id=student_id)

    data = [{
        "sender": m.sender,
        "message": m.message,
        "read_status": m.read_status,
        "time": localtime(m.timestamp).strftime("%I:%M %p")
    } for m in messages]

    return JsonResponse({"messages": data})


@csrf_exempt
def send_message(request, student_id):
    data = json.loads(request.body)

    ChatMessage.objects.create(
        sender="teacher",
        student_id=student_id,
        message=data["message"]
    )

    return JsonResponse({"status": "success"})


@csrf_exempt
def clear_chat(request, student_id):
    ChatMessage.objects.filter(student_id=student_id).delete()
    return JsonResponse({"status": "cleared"})


def AdminLoginPage(request):
    return render(request, "adminlogin.html")


def AdminLogin(request):
    if request.method == 'POST':
        admin_username = request.POST.get('admin_username')
        admin_password = request.POST.get('admin_password')

        if User.objects.filter(username__contains=admin_username).exists():
            data = authenticate(username=admin_username, password=admin_password)

            if data is not None:
                login(request, data)
                request.session['Username'] = admin_username
                messages.success(request, "Admin Login Successfully")
                return redirect(Indexpage)

            else:
                messages.warning(request, "Incorrect Username or Password!")
                return redirect(AdminLoginPage)
        else:
            messages.warning(request, "Username Doesn't exist!")
            return redirect(AdminLoginPage)


def AdminLogout(request):
    del request.session['Username']
    messages.success(request, "Admin Logout Successfully")
    return redirect(AdminLoginPage)
