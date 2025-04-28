from .views.payment_view import *
from app.views import *
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import  DefaultRouter
from .views.attendance_view import *
from .views.attendance_view import AttendanceCreateAPIView
from .views.group_views import *
from .views.statistika_views import *
from app.views.student_view import StudentApi
from app.views.view_teach import Teacher_Api
from .views.homework_views import *
router=DefaultRouter()


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("",include(router.urls)),
    path('PaymentStatisticsView/',PaymentStatisticsView.as_view()),
    path('GroupStudentStatistikaView/',GroupStudentStatistikaView.as_view()),
    path('HomeworkStudentAPIView/',HomeworkStudentAPIView.as_view()),
    path('PaymentAPIView/',PaymentAPIView.as_view()),
    path('attendanceStudent/',AttendanceCreateAPIView.as_view()),
    path("student_api/",StudentApi.as_view()),
    path('HomeworkCreateAPIView/',HomeworkCreateAPIView.as_view()),
    path('TeacherAttendanceAPIView/',TeacherAttendanceAPIView.as_view()),
    path("get_phone/",PhoneSendOTP.as_view()),
    path("post_phone/",VerifySMS.as_view()),
    path("groupapi/",GroupApi.as_view()),
    path('TeacherApi/',Teacher_Api.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("loginApi/",LoginApi.as_view()),

]



