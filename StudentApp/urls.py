from django.urls import path
from StudentApp import views

urlpatterns = [
    path('StudentHomePage/', views.StudentHomePage, name="StudentHomePage"),

    path('StudentReportPage/', views.StudentReportPage, name="StudentReportPage"),
    path('DownloadInternalPdf/', views.DownloadInternalPdf, name="DownloadInternalPdf"),

    path('StudentAttendanceDisplayPage/', views.StudentAttendanceDisplayPage, name="StudentAttendanceDisplayPage"),

    path("chat/", views.StudentChatPage, name="StudentChatPage"),
    path("chat/get/", views.get_student_messages, name="get_student_messages"),
    path("chat/send/", views.send_student_message, name="send_student_message"),
    path("chat/clear/", views.clear_student_chat, name="clear_student_chat"),

    path('StudentLoginPage/', views.StudentLoginPage, name="StudentLoginPage"),
    path('StudentLogin/', views.StudentLogin, name="StudentLogin"),
    path('StudentLogout/', views.StudentLogout, name="StudentLogout"),
]
