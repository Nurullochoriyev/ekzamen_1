from django.contrib import admin
from .models.model_payment import *
from .models import GroupStudent, Student
from .models.model_attendance import Attendance, StudentAttendance, TeacherAttendance, TAttendance
from .models.model_homework import *
from  .models.model_teacher import *
from  .models.auth_users import *
from .models.model_group import *
admin.site.register([User,Departments,Teacher,Course,GroupStudent,Table,Rooms,
                     TableType,Student,Attendance,StudentAttendance,
                     TeacherAttendance,TAttendance,Homework,Topshiriq,Month,Payment])

#
#
#
#
#
# # server{
# #     listen 80;
# #     server_name 165.22.27.171;
# #     lacation=/favicon.ico{access_log off; log_not_found off; }
# #     lacation/static/ {
# #         root/var/www/egzamen_1;
# #
# #     }
# #     lacation / {
# #         include proxy_params;
# #         proxy_pass http://unix:/run/gunicorn.sock;
# #     }
# # }




# a=[1,2,3,4,5,6]
# b=[i  for i in a if i%2]
# print(b)
# a={
#     1:10,
#     2:11,
#     3:12
# }
#
# b={i:k for i,k in a.items() if k%2}
# print(b)
#
#
# a=[1,2,3,4,5,6]
# s=list(str(a))
# print(s)
