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


]