# DRFdan kerakli klasslar va modullar import qilinmoqda
from rest_framework.viewsets import ModelViewSet  # CRUD uchun ViewSet
from rest_framework.permissions import IsAuthenticated  # Foydalanuvchi avtorizatsiyadan o'tganini tekshirish
from rest_framework.response import Response  # Javob qaytarish uchun
from rest_framework import status  # Status kodlari (200, 201, 400 va boshqalar)

# App ichidagi model va serializerlarni import qilish
from app.models import GroupStudent  # GroupStudent modeli
from app.serializers.group_serializer import GroupSerializer  # Group uchun serializer
from ..permissions import IsAdminOrTeacherLimitedEdit  # Maxsus ruxsat sinfi (Admin yoki cheklangan teacher)

# Guruh (GroupStudent) uchun to‘liq CRUD ViewSet (ModelViewSet asosida)
class GroupStudentViewSet(ModelViewSet):  # GROUP uchun CRUD amallar
    queryset = GroupStudent.objects.all().order_by('-id')  # Barcha group yozuvlarini ID bo‘yicha teskari tartibda olish
    serializer_class = GroupSerializer  # Ushbu model uchun foydalaniladigan serializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacherLimitedEdit]  # Ruxsat: foydalanuvchi avtorizatsiyadan o'tgan bo'lishi va admin/teacher bo'lishi kerak

    # GROUP YARATISH (POST metodi)
    def create(self, request, *args, **kwargs):
        data = request.data.copy()  # Yuborilgan ma’lumotni nusxalash

        # Agar 'teacher' maydoni string bo‘lsa (masalan: "1,2,3") uni listga aylantirish
        if isinstance(data.get('teacher'), str):
            data['teacher'] = [t.strip() for t in data['teacher'].split(',')]  # "1,2" → ["1", "2"]

        serializer = self.get_serializer(data=data)  # Serializerga ma'lumot berish
        serializer.is_valid(raise_exception=True)  # Validatsiya; noto‘g‘ri bo‘lsa avtomatik xatolik
        self.perform_create(serializer)  # Ma'lumotni bazaga saqlash
        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 201 Created javobini qaytarish

    # GROUP YANGILASH (PUT yoki PATCH metodi)
    def update(self, request, *args, **kwargs):
        data = request.data.copy()  # So‘rov ma'lumotlarini nusxalash

        # Teacher maydoni string bo‘lsa, listga o‘tkazish
        if isinstance(data.get('teacher'), str):
            data['teacher'] = [t.strip() for t in data['teacher'].split(',')]

        partial = kwargs.pop('partial', False)  # PATCH bo‘lsa qisman yangilash
        instance = self.get_object()  # Yangilanayotgan obyektni olish
        serializer = self.get_serializer(instance, data=data, partial=partial)  # Serializerga yangi ma’lumotni berish
        serializer.is_valid(raise_exception=True)  # Validatsiya qilish
        self.perform_update(serializer)  # Obyektni yangilash
        return Response(serializer.data)  # Muvaffaqiyatli javob qaytarish























#
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.views import APIView
# from app.add_pagination import CustomPagination
# from app.models import GroupStudent
# from app.serializers.group_serializer import GroupSerializer
# from rest_framework.permissions import IsAuthenticated
# from ..permissions import IsAdminOrTeacherLimitedEdit
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
#
#
# class GroupApi(APIView):
#     @swagger_auto_schema(request_body=GroupSerializer)
#     def post(self, request):
#         data = request.data.copy()
#
#         if isinstance(data.get('teacher'), str):
#             data['teacher'] = [t.strip() for t in data['teacher'].split(',')]
#
#         serializer = GroupSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         group_title = GroupStudent.objects.all().order_by('-id')
#         paginator = CustomPagination()
#         paginator.page_size = 2
#         result_page = paginator.paginate_queryset(group_title, request)
#         serializer = GroupSerializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data)
#
#
#
# class GroupStudentDetailUpdateAPIView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminOrTeacherLimitedEdit]
#     @swagger_auto_schema(request_body=GroupSerializer)
#     def patch(self, request, pk):
#         group = get_object_or_404(GroupStudent, pk=pk)
#         self.check_object_permissions(request, group)
#         serializer = GroupSerializer(group, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#
#     @swagger_auto_schema(request_body=GroupSerializer)
#     def put(self, request, pk):
#         group = get_object_or_404(GroupStudent, pk=pk)
#         self.check_object_permissions(request, group)
#         serializer = GroupSerializer(group, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)