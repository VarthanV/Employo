from django.urls import path
from . import  views
urlpatterns=[
    path('login/',views.LoginView.as_view()),
    path('employeeregister/',views.EmployeeRegisterView.as_view()),
    path('employerregister/',views.EmployeeRegisterView.as_view())
]