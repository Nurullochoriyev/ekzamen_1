
from app.views import *
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import  DefaultRouter

from app.views.view_teach import Crud_Teacher

router=DefaultRouter()


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("",include(router.urls)),
    path("get_phone/",PhoneSendOTP.as_view()),
    path("post_phone/",VerifySMS.as_view()),
    path('crud_teacher/',Crud_Teacher.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("loginApi/",LoginApi.as_view()),

]
