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
from app.views.view_teach import Teacher_Api, Name
from .views.homework_views import *
router=DefaultRouter()
router.register('groups', GroupStudentViewSet)
router.register(r'users', UserViewSet, basename='users')



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# URL patterns
urlpatterns = [
    path("", include(router.urls)),

    # Auth & JWT
    path('Name/',Name.as_view()),
    path("loginApi/", LoginApi.as_view()),
    path("get_phone/", PhoneSendOTP.as_view()),
    path("post_phone/", VerifySMS.as_view()),
    path("ChangePasswordView/", ChangePasswordView.as_view()),
    path('SetPasswordView/',SetPasswordView.as_view()),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Student & Teacher
    path("B_student_api/", StudentApi.as_view()),
    path("B_TeacherApi/", Teacher_Api.as_view()),

    # Attendance
    path("C_attendanceStudent/", AttendanceCreateAPIView.as_view()),
    path('C_AttendanceStudentPatch/<int:attendance_id>/',AttendanceStudentPatch.as_view()),
    path("C_TeacherAttendanceAPIView/", TeacherAttendanceAPIView.as_view()),
    path('C_Teacher-attendancePATCH/<int:attendance_id>/', TeacherAttendanceAPIViewPatch.as_view()),

    # Homework
    path("A_HomeworkCreateAPIView/", HomeworkCreateAPIView.as_view()),
    path("A_HomeworkStudentAPIView/", HomeworkStudentAPIView.as_view()),
    path("A_baholash/<int:student_id>/", Baholash.as_view()),
    path("A_BahoniKorish/<int:topshiriq_id>/", BahoniKorish.as_view()),
    path("A_baholashuchunkorish/homework/<int:homework_id>/", UyVazifasiniTekshirishAPIView.as_view(), name="tekshirish-list"),

    # Group & Stats
    # path("groupapi/", GroupApi.as_view()),
    path("PaymentStatisticsView/", PaymentStatisticsView.as_view()),
    path("GroupStudentStatistikaView/", GroupStudentStatistikaView.as_view()),
    path("PaymentAPIView/", PaymentAPIView.as_view()),
    # path('GroupStudentDetailUpdateAPIView/',GroupStudentDetailUpdateAPIView.as_view()),
]


