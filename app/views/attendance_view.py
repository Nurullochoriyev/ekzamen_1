
from rest_framework import status, permissions

from rest_framework.views import APIView
from ..serializers.attendance_serializers import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

# STUDENT ATTENDANCE ISHLAYAPDI

class AttendanceCreateAPIView(APIView):
    @swagger_auto_schema(responses={200: StudentAttendanceListSerializer(many=True)})
    def get(self, request):
        attendance = StudentAttendance.objects.all()
        serializers = StudentAttendanceListSerializer(attendance, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            attendance = serializer.save()
            return Response({
                'id': attendance.id,
                'group': attendance.group_id,
                'date': attendance.date,
                'descriptions': attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yaratildi'
            }, status=201)
        return Response(serializer.errors, status=400)

#  TEACHER ATTENDANCE ISHLAYAPDI

class TeacherAttendanceAPIView(APIView):
    # permission_classes = [permissions.IsAdminUser]  # faqat adminlar uchun

    @swagger_auto_schema(responses={200: TAttendanceSerializer(many=True)})
    def get(self, request):
        attendances = TeacherAttendance.objects.select_related('teacher__user', 'attendance__group',
                                                               'attendance').order_by('-attendance__date')
        serializer = TAttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TeacherAttendanceBulkSerializer)
    def post(self,request):
        serializer=TeacherAttendanceBulkSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            attendance=serializer.save()
            return Response({
                'id':attendance.id,
                # 'teacher':attendance.teacher,
                'date':attendance.date,
                'descriptions': attendance.descriptions,
                'message': 'Davomat muvaffaqiyatli yaratildi'

            },status=201)
        return Response(serializer.errors,status=400)