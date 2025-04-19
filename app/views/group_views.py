
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from app.add_pagination import CustomPagination
from app.models import GroupStudent
from app.serializers.group_serializer import GroupSerializer
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminOrTeacherLimitedEdit
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class GroupApi(APIView):
    @swagger_auto_schema(request_body=GroupSerializer)
    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        group_title = GroupStudent.objects.all().order_by('-id')
        paginator = CustomPagination()
        paginator.page_size = 2
        result_page = paginator.paginate_queryset(group_title, request)
        serializer = GroupSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class GroupStudentDetailUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrTeacherLimitedEdit]
    @swagger_auto_schema(request_body=GroupSerializer)
    def patch(self, request, pk):
        group = get_object_or_404(GroupStudent, pk=pk)
        self.check_object_permissions(request, group)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
