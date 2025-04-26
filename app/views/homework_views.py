
import copy

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..models.model_homework import Homework
from ..serializers.homework_serializer import *

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class HomeworkCreateAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklash uchun
    """
    O'qituvchi yangi uy vazifasi yaratadi.
    """
    @swagger_auto_schema(responses={200:TopshirishSerializer(many=True)})
    def get(self,request):
        homework=Topshiriq.objects.all()
        serializer=TopshirishSerializer(homework,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=HomeWorkSerializer,  # Faqat request_body ishlatilmoqda
        operation_description="Yangi uy vazifasi yaratish. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},

        consumes = ["multipart/form-data"]  # Muhim!
    )

    def post(self, request):
        serializer = HomeWorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkStudentAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # Fayl yuklash uchun

    @swagger_auto_schema(responses={200: HomeWorkSerializer(many=True)})
    def get(self, request):
        homework = Homework.objects.all()
        serializer = HomeWorkSerializer(homework, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        request_body=TopshirishSerializer,  # Faqat request_body ishlatilmoqda
        operation_description="Yangi uy vazifasi yuklandi. Fayl yuklash uchun multipart/form-data formatidan foydalaning.",
        responses={201: 'saqlandi'},
        consumes = ["multipart/form-data"]  # Muhim!
    )
    def post(self,request):
        serializer=TopshirishSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
















#
# a=[[1,2,3],[3,4,5]]
#
# c=copy.copy(a)
# d=copy.deepcopy(a)
# a[0][0]=55
# print(a,id(a))
# print(c,id(c))
# print(d,id(d))
