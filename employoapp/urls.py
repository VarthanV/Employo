from django.urls import path
from . import views
urlpatterns=[
    path('', views.HomeView.as_view(),name='home'),
    path('addemployee/',views.EmployeeRegisterView.as_view(),name='add-employee'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('addemployer/',views.EmployerRegisterView.as_view(),name='add-employer'),
    path('profile/<int:pk>/',views.ProfileView.as_view(),name='profile')


]