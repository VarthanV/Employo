from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .models import Employee, Skill, Profile, Employer, Jobs, JobSkill
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.contrib.auth import login, authenticate, logout, get_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.http import HttpResponse, Http404


class HomeView(View):
    template_name = "employoapp/index.html"

    def get(self, request):
        jobs = Jobs.objects.all()

        return render(request, self.template_name, {'jobs': jobs})


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

        if not request.user.profile.employer:
            return HttpResponse(status=500)
        return render(request, self.template_name)

    def post(self, request):

        if not request.user.profile.employer:
            return HttpResponse(status=500)
        else:
            employer = get_object_or_404(
                Employer, user=User.objects.get(pk=request.user.pk))
            job = Jobs()
            job.title = request.POST.get('title')
            job.about = request.POST.get('about')
            job.location = request.POST.get('location')
            job.company = request.POST.get('company')
            job.employer = employer.user
            job.files = request.FILES.get('files')
            job.save()
            for skill in request.POST.get('skills').split(','):
                skill, d = JobSkill.objects.get_or_create(
                    skill=skill, job=job)

                skill.save()

            return redirect('job-detail', pk=job.pk)


class ProfileView(View):
    template_name = "employoapp/profile.html"

    def get(self, request, pk):
        user = User.objects.get(pk=pk)

        if not request.user.pk == user.pk:
            return HttpResponse(status=500)
        if request.user.profile.employee:
            employee = get_object_or_404(Employee, user=user)

            return render(request, self.template_name, {'employee': employee, 'isemployee': True})

        elif request.user.profile.employer:
            employer = get_object_or_404(Employer, user=user)

            return render(request, self.template_name, {'employer': employer, 'isemployer': True, })
        else:
            return HttpResponse(status=500)

    def post(self, request, pk):
        user = User.objects.get(pk=pk)
        employee = get_object_or_404(Employee, user=user)
        employee.resume = request.FILES.get('docfile')
        employee.save()
        return redirect('profile', pk=pk)
        return render(request, self.template_name, {'employee': employee, 'isemployee': True})


@csrf_exempt
@require_GET
def resumeRemoveView(request, pk):
    user = User.objects.get(pk=pk)
    employee = get_object_or_404(Employee, user=user)

    employee.resume.delete()
    employee.save()
    return redirect('profile', pk=pk)


class JobDetailView(View, LoginRequiredMixin):
    template_name = "employoapp/job_detail.html"

    def get(self, request, pk):
        job = Jobs.objects.get(pk=pk)
        employer = Employer.objects.get(user=job.employer)
        return render(request, self.template_name, {'job': job, 'employer': employer})


class EmployeeEditView(View, LoginRequiredMixin, UserPassesTestMixin):

    template_name = "employoapp/employeeedit.html"

    def test_func(self):
        employee = Employee.objects.get(pk=self.kwargs['pk'])
        return self.request.user.pk == employee.pk

    def get(self, request, pk):
        employee = Employee.objects.get(user=request.user)
        return render(request, self.template_name, {'employee': employee})
