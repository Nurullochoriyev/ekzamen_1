from http.client import responses

from rest_framework import status
from rest_framework.views import APIView
from ..serializers.attendance_serializers import *
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

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