from django.contrib.messages.context_processors import messages
from django.shortcuts import render, redirect
from TeacherApp.models import Studentdb, Internalmarkdb, ChatMessage, Attendancedb, Subjectdb
from django.contrib import messages

from TeacherApp.utils.pdf_generator import generate_pdf_table
from django.http import FileResponse
from reportlab.lib import colors

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from TeacherApp.models import ChatMessage

# Create your views here.
def StudentHomePage(request):
    student = Studentdb.objects.get(id=request.session['StudentId'])
    if not student:
        messages.error(request, "please Login !")
        return redirect(StudentLoginPage)
    return render(request, "base.html", {'student': student})


def StudentReportPage(request):
    # get student id
    student = Studentdb.objects.get(id=request.session['StudentId'])
    internal = Internalmarkdb.objects.filter(Student=request.session['StudentId'])

    attendance = []

    for i in internal:
        # fetches sub id
        subject = i.Subject
        Total_class = Attendancedb.objects.filter(Student=student, Subject=subject).count()
        present_class = Attendancedb.objects.filter(Student=student, Subject=subject, Status="Present").count()
        if Total_class == 0:
            percentages = 0
        else:
            percentages = round((present_class / Total_class) * 100)
        attendance.append({'subject': subject.Subject_name,
                           'subjectcode': subject.Subject_code,
                           'internalmark': i.Internalmark,
                           'totalmark': i.Totalmark,
                           'percentages': percentages})

    return render(request, 'StudentReport.html', {'student': student, 'internal': internal, 'attendance': attendance})


def DownloadInternalPdf(request):
    student = Studentdb.objects.get(id=request.session['StudentId'])
    internal = Internalmarkdb.objects.filter(Student=student)

    # Build table header
    data_rows = [
        ["Subject", "Code", "Internal", "Total", "Attendance %"]
    ]

    # Fill rows with marks + attendance
    for i in internal:
        subject = i.Subject

        Total_class = Attendancedb.objects.filter(
            Student=student,
            Subject=subject
        ).count()

        present_class = Attendancedb.objects.filter(
            Student=student,
            Subject=subject,
            Status="Present"
        ).count()

        if Total_class == 0:
            percentages = 0
        else:
            percentages = round((present_class / Total_class) * 100)

        data_rows.append([
            subject.Subject_name,
            subject.Subject_code,
            i.Internalmark,
            i.Totalmark,
            f"{percentages}%",
        ])

    # Color logic for attendance column
    def attendance_color(cell_value):
        # cell_value like "75%"
        num = int(str(cell_value).replace("%", ""))
        if num < 75:
            return colors.red
        return colors.green

    column_color_map = {
        4: attendance_color  # 0-based index → 4th column = "Attendance %"
    }

    pdf_buffer = generate_pdf_table(
        title='',
        data_rows=data_rows,
        column_color_map=column_color_map
    )

    filename = f"{student.Student_name}_Internal_Report.pdf"
    return FileResponse(pdf_buffer, as_attachment=True, filename=filename)


def StudentAttendanceDisplayPage(request):
    student_id = request.session.get('StudentId')
    if student_id:
        student = Studentdb.objects.get(id=student_id)

    attendance = []
    subjects = Subjectdb.objects.all()

    for i in subjects:
        total = Attendancedb.objects.filter(Student=student, Subject=i).count()
        present = Attendancedb.objects.filter(Student=student, Subject=i, Status='Present').count()
        percentage = round((present / total) * 100) if total > 0 else 0

        attendance.append({
            'subject_name': i.Subject_name,
            'subject_code': i.Subject_code,
            'percentage': percentage
        })

    # For donut (right side) : first subject
    default = attendance[0] if attendance else None

    return render(request, 'StudentAttendanceDisplay.html', {
        'attendance': attendance,
        'default': default
    })

def StudentChatPage(request):
    student_id = request.session.get("StudentId")
    if not student_id:
        return redirect("StudentLoginPage")

    # Mark teacher messages as READ
    ChatMessage.objects.filter(
        student_id=student_id,
        sender="teacher",
        read_status="delivered"
    ).update(read_status="read")

    return render(request, "student_chat.html")


def get_student_messages(request):
    student_id = request.session.get("StudentId")

    # Mark teacher messages as DELIVERED
    ChatMessage.objects.filter(
        student_id=student_id,
        sender="teacher",
        read_status="sent"
    ).update(read_status="delivered")

    messages = ChatMessage.objects.filter(student_id=student_id)

    data = [{
        "sender": m.sender,
        "message": m.message,
        "read_status": m.read_status,
        "time": m.timestamp.strftime("%I:%M %p")
    } for m in messages]

    return JsonResponse({"messages": data})


@csrf_exempt
def send_student_message(request):
    student_id = request.session.get("StudentId")
    data = json.loads(request.body)

    ChatMessage.objects.create(
        sender="student",
        student_id=student_id,
        message=data["message"]
    )

    return JsonResponse({"status": "success"})


@csrf_exempt
def clear_student_chat(request):
    student_id = request.session.get("StudentId")
    ChatMessage.objects.filter(student_id=student_id).delete()
    return JsonResponse({"status": "cleared"})



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
