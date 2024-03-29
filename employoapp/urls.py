from django.urls import path
from . import views
urlpatterns=[
    path('', views.HomeView.as_view(),name='home'),
    path('addemployee/',views.EmployeeRegisterView.as_view(),name='add-employee'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('addemployer/',views.EmployerRegisterView.as_view(),name='add-employer'),
    path('profile/<int:pk>/',views.ProfileView.as_view(),name='profile'),
    path('remove/<int:pk>',views.resumeRemoveView,name='resume-remove'),
    path('postjob/',views.JobPostingView.as_view(),name='job-posting'),
    path('job/<int:pk>/',views.JobDetailView.as_view(),name='job-detail'),
    path('employeeedit/<int:pk>/',views.EmployeeEditView.as_view(),name='employee-edit')


]