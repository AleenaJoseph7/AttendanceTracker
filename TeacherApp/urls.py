from django.urls import path
from TeacherApp import views

urlpatterns=[
    path('Indexpage/',views.Indexpage,name="Indexpage"),

    path('Addstudentpage/',views.Addstudentpage,name="Addstudentpage"),
    path('savestudent/',views.savestudent,name="savestudent"),
    path('DisplaystudentPage/',views.DisplaystudentPage,name="DisplaystudentPage"),
    path('EditstudentPage/<int:s_id>',views.EditstudentPage,name="EditstudentPage"),
    path('updatestudent/<int:s_id>',views.updatestudent,name="updatestudent"),
    path('deletestudent/<int:s_id>',views.deletestudent,name="deletestudent"),

    path('AddsubjectPage/',views.AddsubjectPage,name="AddsubjectPage"),
    path('savesubject/',views.savesubject,name="savesubject"),
    path('DisplaysubjectPage/',views.DisplaysubjectPage,name="DisplaysubjectPage"),
    path('EditsubjectPage/<int:sub_id>/',views.EditsubjectPage,name="EditsubjectPage"),
    path('Updatesubject/<int:sub_id>/',views.Updatesubject,name="Updatesubject"),
    path('Deletesubject/<int:sub_id>/',views.Deletesubject,name="Deletesubject"),

    path('Addinternalpage/',views.Addinternalpage,name="Addinternalpage"),
    path('Saveinternal/',views.Saveinternal,name="Saveinternal"),
    path('Displayinternal/',views.Displayinternal,name="Displayinternal"),
    path('Editinternalpage/<int:i_id>/',views.Editinternalpage,name="Editinternalpage"),
    path('Updateinternal/<int:i_id>/',views.Updateinternal,name="Updateinternal"),
    path('Deleteinternal/<int:i_id>/',views.Deleteinternal,name="Deleteinternal"),

    path('AttendancePage/',views.AttendancePage,name="AttendancePage"),
    path('saveattendance/',views.saveattendance,name="saveattendance"),
    path('Displayattendancepage/',views.Displayattendancepage,name="Displayattendancepage"),
    path('Editattendancepage/<int:a_id>/',views.Editattendancepage,name="Editattendancepage"),
    path('updateattendance/<int:a_id>/',views.updateattendance,name="updateattendance"),
    path('deleteattendance/<int:a_id>/',views.deleteattendance,name="deleteattendance"),
    path('AttendancePercentagePage/',views.AttendancePercentagePage,name="AttendancePercentagePage"),

    path("pdf/internal/<int:subject_id>/", views.internal_pdf, name="internal_pdf"),
    path("pdf/student/<int:student_id>/", views.student_attendance_pdf, name="student_attendance_pdf"),
    path("pdf/subject/<int:subject_id>/", views.subject_attendance_pdf, name="subject_attendance_pdf"),


    path('AdminLoginPage/',views.AdminLoginPage,name="AdminLoginPage"),
    path('AdminLogin/',views.AdminLogin,name="AdminLogin"),
    path('AdminLogout/',views.AdminLogout,name="AdminLogout"),

]