import random




from ..make_token import *

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from django.contrib.auth.hashers import make_password
from rest_framework import status

from ..permissions import IsAdmin
from ..serializers import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from ..models import User
from ..serializers import SMSSerializer
from drf_yasg.utils import swagger_auto_schema


# Telefon raqami orqali OTP (tasdiqlash kodi) yuboruvchi API
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
        # Telefon raqam avvaldan ro‘yxatdan o‘tganmi — tekshiradi
        user = User.objects.filter(phone_number__iexact=phone)
        if user.exists():
            return Response({
                'status': False,
                'detail': 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # OTP (tasdiqlash kodi) yuboriladi va 10 daqiqa cache ga saqlanadi
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




# TORT HONALI KOD YARATIB BERADI
def send_otp():
    otp=str(random.randint(1001,9999))
    print(otp,"==========================")
    return otp


from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache


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

# Yangi foydalanuvchini ro‘yxatdan o‘tkazish uchun API
# class RegisterUserApi(APIView):
#     @swagger_auto_schema(request_body=UserSerializer)
#     def post(self,request):
#         serializer=UserSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             password=serializer.validated_data.get('password')
#             serializer.validated_data['password']=make_password(password)
#             serializer.save()
#             return Response({
#                 "status":True,
#                 'datail':'account create'
#             })
#     def get(self,request):
#         users=User.objects.all().order_by("-id")
#         serializer=UserSerializer(users,many=True)
#         return Response(data=serializer.data)
#



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password

# USERNI ROYHATDAN OTKIZADI
class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by("-id")
    serializer_class = UserCrudSerializer
    permission_classes = [AllowAny]  # Kerak bo‘lsa, o‘zgartiring

    # Parolni avtomatik hash qilish
    def perform_create(self, serializer):
        password = serializer.validated_data.get('password')
        serializer.save(password=make_password(password))

    def perform_update(self, serializer):
        password = serializer.validated_data.get('password', None)
        if password:
            serializer.save(password=make_password(password))
        else:
            serializer.save()





 # ChangePasswordView va SetPasswordView ikkala klass ham
# foydalanuvchi parolini yangilashga xizmat qiladi,
# ammo maqsad va xavfsizlik darajalari bo‘yicha farq qiladi.
#  kod Django REST Framework (DRF) dan foydalanib parolni
# o‘zgartirish uchun yozilgan APIView klassidir.
# eski parol talab qilinadi

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def patch(self,request):
        serializer=ChangePasswordSerializer(instance=self.request.user,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# FOYDALANUVCHI PAROLLINI OZGARTIRISH
# qachonki parol unitilganda ishlatiladi
class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SetPasswordSerializer)
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Parol muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ISHLAYAPDI
# YANGI TOKEN YARATISH (OZIMIZ)
# Login API — foydalanuvchiga token yaratib beradi

class LoginApi(APIView):
    permission_classes = [AllowAny,]
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user=serializer.validated_data.get("user")
        token=get_tokens_for_user(user)
        token["salom"]="hi"
        token["is_admin"]=user.is_superuser
        return Response(data=token,status=status.HTTP_200_OK)


