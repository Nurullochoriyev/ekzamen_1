from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.models import GroupStudent
from app.serializers.group_serializer import GroupSerializer
from ..permissions import IsAdminOrTeacherLimitedEdit

class GroupStudentViewSet(ModelViewSet):    #GROUPGA CRUD
    queryset = GroupStudent.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrTeacherLimitedEdit]
#GROUP YARATISH
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        # kelyotgan malumotni stringdan listga o'tkizadi
        if isinstance(data.get('teacher'), str):
            data['teacher'] = [t.strip() for t in data['teacher'].split(',')]

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()

        if isinstance(data.get('teacher'), str):
            data['teacher'] = [t.strip() for t in data['teacher'].split(',')]

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)























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