from django.db import models
from django.contrib.auth.models import User


class Jobs(models.Model):
    title = models.CharField(max_length=200)
    about = models.TextField()
    location = models.CharField(max_length=50)
    employer = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    employee = models.ManyToManyField(User, related_name="employee_set")
    company=models.CharField(max_length=50,blank=True)
    files=models.FileField(blank=True,null=True)
    def __str__(self):
        return self.title




class Employee(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employee')
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    jobs = models.ManyToManyField(
        Jobs, related_name='employee_jobs_set')
    phone_number = models.CharField(max_length=10)
    about = models.TextField(blank=True)
    resume = models.FileField(blank=True)

class JobSkill(models.Model):
    skill=models.CharField(max_length=50)
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE,blank=True,null=True)

class Skill(models.Model):
    skill = models.CharField(max_length=50)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, blank=True,null=True)
    

    def __str__(self):
        return self.skill


class Employer(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='employer')
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    designation = models.CharField(max_length=50, blank=True)
    about = models.TextField(blank=True)
    jobs = models.ManyToManyField(
        Jobs, related_name='employer_jobs_set', blank=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee = models.BooleanField(default=False)
    employer = models.BooleanField(default=False)
    User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])

    def __str__(self):
        return self.user.username
