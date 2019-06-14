from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
import json
from employoapp.models import Employee,Employer,Profile,Skill
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import login,logout,authenticate
from rest_framework.authentication import TokenAuthentication

class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        user=User.objects.get(email=request.POST.get('email'))
        if user is None:
            raise SuspiciousOperation

        user=authenticate(username=user.username,password=request.POST.get('password'))    
        if not user:
            raise SuspiciousOperation
        login(request, user)
        token, dummy = Token.objects.get_or_create(user=user)
      
        return Response({'username': user.username, 'email': user.email, 'token': token.key,'pk':user.pk})

class EmployeeRegisterView(APIView):
    
    permission_classes=(AllowAny,)

    def post(self, request):
        if User.objects.filter(email=request.POST.get('email')).exists():
            raise SuspiciousOperation
        if User.objects.filter(email=request.POST.get('username')).exists():
           raise SuspiciousOperation

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

            return Response({
                "registered":True
            })

class EmployerRegisterView(APIView):
    permission_classes=(AllowAny,)  

   

    def post(self, request):
        if User.objects.filter(email=request.POST.get('email')).exists():
           raise SuspiciousOperation
        elif User.objects.filter(email=request.POST.get('username')).exists():
             raise SuspiciousOperation
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
        
        return Response({
            "registered":True
        })
