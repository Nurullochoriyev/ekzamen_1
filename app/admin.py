from django.contrib import admin

from .models import GroupStudent, Student
from  .models.model_teacher import *
from  .models.auth_users import *
admin.site.register([User,Departments,Teacher,Course,GroupStudent,Student])
