from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count
from ..models.model_payment import *
from ..serializers.statistika_serializer import *
from ..models.model_student import *
class PaymentStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        total_payments = Payment.objects.count()
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


class GroupStudentStatistikaView(APIView):
    def get(self, request, *args, **kwargs):
        current_year = timezone.now().year

        graduated_groups = GroupStudent.objects.filter(end_date__year=2024).count()
        studying_groups = GroupStudent.objects.filter(end_date__gt=timezone.now().date()).count()
        enrolled_groups = GroupStudent.objects.filter(start_date__year=2024).count()

        data = {
            'graduated_groups': graduated_groups,
            'studying_groups': studying_groups,
            'enrolled_groups': enrolled_groups,
        }

        serializer = GroupStudentStatistikaSerializer(data)
        return Response(serializer.data)