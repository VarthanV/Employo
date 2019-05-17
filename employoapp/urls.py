from django.urls import path
from . import views
urlpatterns=[
    path('', views.HomeView.as_view(),name='home'),
    path('addemployee/',views.EmployeeRegisterView.as_view(),name='add-employee')

]