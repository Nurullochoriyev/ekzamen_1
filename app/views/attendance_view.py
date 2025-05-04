from drf_yasg import openapi
from rest_framework import status, permissions
from app.permissions import IsTeacherOfStudentPermission

from rest_framework.views import APIView
from ..serializers.attendance_serializers import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

# STUDENT ATTENDANCE ISHLAYAPDI

class AttendanceCreateAPIView(APIView):
    permission_classes = [IsTeacherOfStudentPermission,IsAuthenticated]
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
class AttendanceStudentPatch(APIView):
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def patch(self, request, attendance_id):
        try:
            attendance = Attendance.objects.get(id=attendance_id)  # ✅ TO‘G‘RI MODEL
        except Attendance.DoesNotExist:
            return Response(
                {'error': 'ID bo‘yicha maʼlumot topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AttendanceCreateSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            updated_attendance = serializer.save()
            return Response(
                {
                    'id': updated_attendance.id,
                    'date': updated_attendance.date,
                    'descriptions': updated_attendance.descriptions,
                    'message': 'Davomat muvaffaqiyatli yangilandi'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  TEACHER ATTENDANCE ISHLAYAPDI

class TeacherAttendanceAPIView(APIView):
    permission_classes = [permissions.IsAdminUser]  # faqat adminlar uchun
# get ishlayapdi
    @swagger_auto_schema(responses={200: TeacherAttendanceSerializer(many=True)})
    def get(self, request):
        attendances = TeacherAttendance.objects.select_related(
            'teacher__user', 'attendance'
        ).order_by('-attendance__date')

        serializer = TeacherAttendanceSerializer(attendances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# post ishlayapdi
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


class TeacherAttendanceAPIViewPatch(APIView):
    permission_classes = [permissions.IsAdminUser]  # faqat adminlar uchun
    @swagger_auto_schema(
        request_body=TeacherAttendanceBulkSerializer,
        manual_parameters=[
            openapi.Parameter(
                'attendance_id',
                openapi.IN_PATH,
                description="TAttendance ID raqami",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: TeacherAttendanceBulkSerializer,
            404: 'Davomat topilmadi',
            400: 'Noto\'g\'ri so\'rov'
        }
    )
    def patch(self, request, attendance_id):
        try:
            attendance = TAttendance.objects.get(id=attendance_id)
        except TAttendance.DoesNotExist:
            return Response(
                {'error': 'Berilgan IDga mos davomat topilmadi'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherAttendanceBulkSerializer(
            attendance,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            updated_attendance = serializer.save()
            return Response(
                {
                    'id': updated_attendance.id,
                    'date': updated_attendance.date,
                    'descriptions': updated_attendance.descriptions,
                    'message': 'Davomat muvaffaqiyatli yangilandi'
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)