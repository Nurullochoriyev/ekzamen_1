
from app.views import *
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import  DefaultRouter

from app.views.student_view import StudentApi
from app.views.view_teach import TeacherApi

router=DefaultRouter()


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("",include(router.urls)),
    path("student_api/",StudentApi.as_view()),
    path("get_phone/",PhoneSendOTP.as_view()),
    path("post_phone/",VerifySMS.as_view()),
    path('TeacherApi/',TeacherApi.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("loginApi/",LoginApi.as_view()),

]
