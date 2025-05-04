from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from ..models.model_payment import *
from ..permissions import IsStaffUser
from ..serializers.statistika_serializer import *
from ..models.model_student import *
class PaymentStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        total_payments = Payment.objects.count()     #TOLOV TIZIMINI STATISTIKASINI OLADI
        total_paid = Payment.objects.filter(status='paid').count()
        total_unpaid = Payment.objects.filter(status='unpaid').count()
        total_partial = Payment.objects.filter(status='partial').count()
        total_cancelled = Payment.objects.filter(status='cancelled').count()
        total_amount = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0

        data = {
            'total_payments': total_payments,
            'total_paid': total_paid,
            'total_unpaid': total_unpaid,
            'total_partial': total_partial,
            'total_cancelled': total_cancelled,
            'total_amount': total_amount,
        }

        serializer = PaymentStatisticsSerializer(data)
        return Response(serializer.data)


# class GroupStudentStatistikaView(APIView):
    # def get(self, request, *args, **kwargs):
    #     current_year = timezone.now().year
    #
    #     graduated_groups = GroupStudent.objects.filter(end_date__year=2024).count()
    #     studying_groups = GroupStudent.objects.filter(end_date__gt=timezone.now().date()).count()
    #     enrolled_groups = GroupStudent.objects.filter(start_date__year=2024).count()
    #
    #     data = {
    #         'graduated_groups': graduated_groups,
    #         'studying_groups': studying_groups,
    #         'enrolled_groups': enrolled_groups,
    #     }
    #
    #
    #     return Response(data)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from app.models import Student, GroupStudent
from rest_framework.permissions import IsAuthenticated
class GroupStudentStatistikaView(APIView):
    permission_classes = [IsStaffUser,IsAuthenticated]
    # VAQT ORALIGIDAGI STATISTIKANI OLISH BASHLANISH VAQTI VA TUGASH VAQTI
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Boshlanish sanasi (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="Tugash sanasi (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        start_date_str = request.query_params.get('start_date')    #OQISHGA KIRGAN VQT
        end_date_str = request.query_params.get('end_date')        #TUGATISH VAQTI

        if not start_date_str or not end_date_str:
            return Response(
                {"error": "start_date va end_date query parametrlari kerak (YYYY-MM-DD formatda)"},
                status=400
            )

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return Response(
                {"error": "Sanalar noto‘g‘ri formatda. To‘g‘ri format: YYYY-MM-DD"},
                status=400
            )





        enrolled_groups = GroupStudent.objects.filter(start_date__range=(start_date, end_date))
        graduated_groups = GroupStudent.objects.filter(end_date__range=(start_date, end_date))

        enrolled_students = Student.objects.filter(group__in=enrolled_groups).distinct().count()
        graduated_students = Student.objects.filter(group__in=graduated_groups).distinct().count()
        active_students = Student.objects.filter(user__is_active=True).count()

        data = {
            "enrolled_students": enrolled_students,
            "graduated_students": graduated_students,
            "active_students": active_students,
        }

        return Response(data)
