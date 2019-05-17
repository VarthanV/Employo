from django.db import models
from django.contrib.auth.models import User
 

class Jobs(models.Model):
    title=models.CharField(max_length=200)
    about=models.TextField()
    location=models.CharField(max_length=50)
    employer=models.ManyToManyField(User,related_name='employers_set')
    employee=models.ManyToManyField(User,related_name="employee_set")


class Employee(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='employee')
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=100)
    location=models.CharField(max_length=50)
    jobs=models.ManyToManyField(Jobs,related_name='employee_jobs_set')   
    phone_number=models.CharField(max_length=10)
    about=models.TextField(blank=True) 
    resume=models.FileField()

class Skill(models.Model):
     skill=models.TextField()
     employee=models.ForeignKey(Employee,on_delete=models.CASCADE)  
     def __str__(self):
          return self.skill 
class Employer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='employer')
    firstName=models.CharField(max_length=50)
    lastName=models.CharField(max_length=100)
    location=models.CharField(max_length=50)
    company_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10) 
    designation=models.CharField(max_length=50,blank=True)
    about=models.TextField(blank=True)
    jobs=models.ManyToManyField(Jobs,related_name='employer_jobs_set')
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    employee=models.BooleanField(default=False)
    employer=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
