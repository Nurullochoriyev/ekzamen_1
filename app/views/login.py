import random


import permission

from ..make_token import *

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.hashers import make_password
from rest_framework import status,permissions
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from ..models import User
from ..serializers import SMSSerializer
from drf_yasg.utils import swagger_auto_schema


# class PhoneSendOTP(APIView):
#     @swagger_auto_schema(request_body=SMSSerializer)
#     def post(self, request, *args, **kwargs):
#         phone_number = request.data.get('phone_number')
#
#         if not phone_number:
#
#
#             phone = str(phone_number)
#             user = User.objects.filter(phone_number__iexact=phone)
#             if user.exists():
#                 return Response({
#                     'status': False,
#                     'detail': 'Phone number already exists'
#                 })
#             else:
#                 key = send_otp()
#                 if key:
#                     cache.set(phone, key, 600)
#                     return  Response({"message":"sms sent successfully"},status=status.HTTP_200_OK)
#                 return Response({"message":"failed to send sms"},status=status.HTTP_400_BAD_REQUEST)
#

class PhoneSendOTP(APIView):
    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({
                'status': False,
                'detail': 'Telefon raqam kiritilmadi'
            }, status=status.HTTP_400_BAD_REQUEST)

        phone = str(phone_number)
        user = User.objects.filter(phone_number__iexact=phone)
        if user.exists():
            return Response({
                'status': False,
                'detail': 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            key = send_otp()
            if key:
                cache.set(phone, key, 600)
                return Response({
                    "status": True,
                    "message": "SMS muvaffaqiyatli yuborildi"
                }, status=status.HTTP_200_OK)
            return Response({
                "status": False,
                "message": "SMS yuborishda xatolik yuz berdi"
            }, status=status.HTTP_400_BAD_REQUEST)


        # try:
        #     key = send_otp()
        #     if key:
        #         # Store the verification code and phone number in cache for 10 minutes (600 seconds)
        #         cache.set(phone_number, key, 600)
        #         return Response({
        #             'status': True,
        #             'detail': 'OTP sent successfully'
        #         } , status=status.HTTP_200_OK)
        #     return Response({"message":"failed to sent sms"},status=status.HTTP_400_BAD_REQUEST)
        #




def send_otp():
    otp=str(random.randint(1001,9999))
    print(otp,"==========================")
    return otp


from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache

#
# class VerifySMS(APIView):
#     @swagger_auto_schema(request_body=VerifySMSSerializer)
#     def post(self, request):
#         serializer = VerifySMSSerializer(data=request.data)
#         if not serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             verification_code = serializer.validated_data['verification_code']
#             cached_code = str(cache.get(phone_number))
#             if verification_code == str(cached_code):
#                 return Response({
#                     'status': True,
#                     'detail': 'OTP matched. Please proceed for registration'
#                 })
#             else:
#                 return Response({
#                     'status': False,
#                     'detail': 'OTP incorrect'
#                 })
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#
class VerifySMS(APIView):
    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))

            if verification_code == cached_code:
                return Response({
                    'status': True,
                    'detail': 'OTP mos tushdi. Ro‘yxatdan o‘tishni davom ettiring.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'detail': 'Noto‘g‘ri tasdiqlash kodi.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # Bu yerda xatolik bo‘lsa, serializer.errors ni qaytaramiz:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApi(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password=serializer.validated_data.get('password')
            serializer.validated_data['password']=make_password(password)
            serializer.save()
            return Response({
                "status":True,
                'datail':'account create'
            })
    def get(self,request):
        users=User.objects.all().order_by("-id")
        serializer=UserSerializer(User,many=True)
        return Response(data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self,request):
        serializer=ChangePasswordSerializer(instance=self.request.user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)










class LoginApi(APIView):
    permission_classes = [AllowAny,]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data.get("user")
        token=get_tokens_for_user(user)
        token["salom"]="hi"
        token["is_admin"]=user.is_superuser
        return Response(data=token,status=status.HTTP_200_OK)


