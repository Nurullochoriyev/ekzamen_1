from drf_yasg import openapi  # Swagger uchun parameterlar ishlatish imkonini beradi
from drf_yasg.utils import swagger_auto_schema  # Swagger uchun view funksiyalarini bezash
from rest_framework.views import APIView  # DRF APIView bazaviy class
from rest_framework.response import Response  # API javoblari uchun
from django.db.models import Sum, Count  # Modeldan umumiy yig‘indi va sanash uchun
from ..models.model_payment import *  # Payment modelini chaqirish
from ..permissions import IsStaffUser  # Maxsus ruxsatlar uchun permission class
from ..serializers.statistika_serializer import *  # Statistika uchun serializer
from ..models.model_student import *  # Talabalar modeli

# === TO'LOVLAR BO'YICHA STATISTIKA ===
class PaymentStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        total_payments = Payment.objects.count()  # Barcha to‘lovlar soni
        total_paid = Payment.objects.filter(status='paid').count()  # To‘langan to‘lovlar soni
        total_unpaid = Payment.objects.filter(status='unpaid').count()  # To‘lanmagan to‘lovlar soni
        total_partial = Payment.objects.filter(status='partial').count()  # Qisman to‘langan to‘lovlar soni
        total_cancelled = Payment.objects.filter(status='cancelled').count()  # Bekor qilingan to‘lovlar soni
        total_amount = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0  # Jami to‘langan summa

        data = {
            'total_payments': total_payments,  # Barcha to‘lovlar
            'total_paid': total_paid,  # To‘langan
            'total_unpaid': total_unpaid,  # To‘lanmagan
            'total_partial': total_partial,  # Qisman
            'total_cancelled': total_cancelled,  # Bekor qilingan
            'total_amount': total_amount,  # Jami summa
        }

        serializer = PaymentStatisticsSerializer(data)  # Ma'lumotni serializerga berish
        return Response(serializer.data)  # Javob qaytarish


# === O'QUVCHI VA GURUH STATISTIKASI (VAQT ORALIG'IDA) ===
from rest_framework.views import APIView  # APIView bazaviy class
from rest_framework.response import Response  # Response klassi
from django.utils.dateparse import parse_date  # Sana parsing uchun
from app.models import Student, GroupStudent  # Student va GroupStudent modellari
from rest_framework.permissions import IsAuthenticated  # Avtorizatsiya tekshiruvi

class GroupStudentStatistikaView(APIView):
    permission_classes = [IsStaffUser, IsAuthenticated]  # Faqat xodimlar va avtorizatsiyalanganlar uchun

    # Swagger uchun GET parametrlarni aniqlash (sana filtrlari)
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
        start_date_str = request.query_params.get('start_date')  # So‘rovdan boshlanish sanasini olish
        end_date_str = request.query_params.get('end_date')  # So‘rovdan tugash sanasini olish

        # Agar sanalar berilmagan bo‘lsa, xato qaytarish
        if not start_date_str or not end_date_str:
            return Response(
                {"error": "start_date va end_date query parametrlari kerak (YYYY-MM-DD formatda)"},
                status=400
            )

        # Sanalarni parse qilish (string -> date)
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        # Agar noto‘g‘ri formatda bo‘lsa, xato
        if not start_date or not end_date:
            return Response(
                {"error": "Sanalar noto‘g‘ri formatda. To‘g‘ri format: YYYY-MM-DD"},
                status=400
            )

        # Belgilangan sanalar oralig‘ida boshlagan guruhlar
        enrolled_groups = GroupStudent.objects.filter(start_date__range=(start_date, end_date))

        # Belgilangan oralig‘da yakunlangan guruhlar
        graduated_groups = GroupStudent.objects.filter(end_date__range=(start_date, end_date))

        # Ro‘yxatga olingan talabalar soni (enrolled)
        enrolled_students = Student.objects.filter(group__in=enrolled_groups).distinct().count()

        # Bitirgan talabalar soni (graduated)
        graduated_students = Student.objects.filter(group__in=graduated_groups).distinct().count()

        # Hozir faol (is_active=True) talabalar
        active_students = Student.objects.filter(user__is_active=True).count()

        data = {
            "enrolled_students": enrolled_students,  # Ro‘yxatga olinganlar
            "graduated_students": graduated_students,  # Bitirganlar
            "active_students": active_students,  # Faol talabalar
        }

        return Response(data)  # JSON formatda javob
