from django.contrib import admin
from .models import Skill,Employee,Profile,Employer

# Register your models here.
admin.site.register(Skill)
admin.site.register(Employee)
admin.site.register(Profile)
admin.site.register(Employer)