from django.urls import path
from StudentApp import views

urlpatterns=[
    path('StudentHomePage/',views.StudentHomePage,name="StudentHomePage"),
]