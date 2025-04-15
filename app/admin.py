from django.contrib import admin

from .models import GroupStudent, Student
from  .models.model_teacher import *
from  .models.auth_users import *
from .models.model_group import *
admin.site.register([User,Departments,Teacher,Course,GroupStudent,Table,TableType,Student])
