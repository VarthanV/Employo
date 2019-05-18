from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Employee, Skill, Profile, Employer
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponse


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
            employee.about = request.POST.get('about')
            employee.save()
            #
            # Profile Logic
            profile = Profile()
            profile.employee = True
            profile.user = user
            profile.save()

            # Skill logic
            for skill in request.POST.get('skills').split(','):
                skill, d = Skill.objects.get_or_create(
                    skill=skill, employee=employee)

                skill.save()

            return redirect('login')
        return render(request, self.template_name)


class LoginView(View):
    template_name = "employoapp/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            user = User.objects.get(email=request.POST.get('email'))

        except:
            return render(request, self.template_name, {'error': True})

        else:
            user = authenticate(request,
                                username=user.username,
                                password=request.POST.get('password')
                                )
            if user is None:
                return render(request, self.template_name, {'error': True})
            login(request, user)

            response = redirect('home')
            response.set_cookie('role', 'user')
            return response

        return render(request, self.template_name)


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        response = redirect('home')
        response.delete_cookie('role')
        return response


class EmployerRegisterView(View):
    template_name = "employoapp/employerregister.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if User.objects.filter(email=request.POST.get('email')).exists():
            return render(request, self.template_name, {'error': True})
        elif User.objects.filter(email=request.POST.get('username')).exists():
            return render(request, self.template_name, {'uerror': True})
        else:
            user = User()
            user.email = request.POST.get('email')
            user.set_password(request.POST.get('password'))
            user.username = request.POST.get('username')
            user.save()
            # Employee Logic
            employer = Employer()
            employer.firstName = request.POST.get('firstname')
            employer.lastName = request.POST.get('lastname')
            employer.phone_number = request.POST.get('phonenumber')
            employer.location = request.POST.get('location')
            employer.user = user
            employer.company_name = request.POST.get('companyname')
            employer.designation = request.POST.get('designation')
            employer.about = request.POST.get('about')

            employer.save()
            #
            # Profile Logic
            profile = Profile()
            profile.user = user
            profile.employer = True
            profile.save()
            return redirect('login')
        return render(request, self.template_name)


class JobPostingView(View):
    template_name = "employoapp/jobposting.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


class ProfileView(View):
    template_name = "employoapp/profile.html"

    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        employee = get_object_or_404(Employee, user=user)
        if not request.user.pk == user.pk:
            raise HttpResponse(status=500)
        if not employee is None:

            return render(request, self.template_name, {'employee': employee, 'isemployee': True})
        elif not employee:
            employer = Employer.objects.get(user=user)
            return render(request, self.template_name, {'employer': employer, 'isemployer': True})
        else:
            return redirect('login')

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        employee = get_object_or_404(Employee, user=user)
        employee.resume = request.FILES.get('docfile')
        employee.save()
        return redirect('profile', pk=employee.pk)
        return render(request, self.template_name, {'employee': employee, 'isemployee': True})
