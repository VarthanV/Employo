from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Employee, Skill, Profile
from django.contrib.auth.models import User


class HomeView(View):
    template_name = "employoapp/index.html"

    def get(self, request):
        return render(request, self.template_name)


class EmployeeRegisterView(View):
    template_name = "employoapp/Employeeregister.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if User.objects.filter(email=request.POST.get('email')).exists():
            return render(request, self.template_name, {'error': True})
        if User.objects.filter(email=request.POST.get('username')).exists():
            return render(request, self.template_name, {'uerror': True})

        else:
            user = User()
            user.email = request.POST.get('email')
            user.set_password(request.POST.get('password'))
            user.username = request.POST.get('username')
            user.save()
            # Employee Logic
            employee = Employee()
            employee.firstName = request.POST.get('firstname')
            employee.lastName = request.POST.get('lastname')
            employee.phone_number = request.POST.get('phonenumber')
            employee.location = request.POST.get('location')
            employee.user = user
            employee.save()
            #
            # Profile Logic
            profile = Profile()
            profile.user = user
            profile.employee = True
            profile.save()

            # Skill logic
            for skill in request.POST.get('skills').split(','):
                skill,d=Skill.objects.get_or_create(skill=skill,employee=employee)
             
                
                skill.save()
                
           
            return redirect('home')
        return render(request, self.template_name)
