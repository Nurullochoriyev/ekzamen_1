from django.utils import timezone
from drf_yasg import openapi
from rest_framework import status

from ..serializers.payment_serializer import *
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response

class PaymentAPIView(APIView):
    @swagger_auto_schema(responses={200:PaymentSerializer(many=True)})
    def get(self,request):
        payment=Payment.objects.all()
        serializer=PaymentSerializer(payment,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=PaymentSerializer)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # To'lovni "paid" holatida yaratish
            payment = serializer.save(
                status='paid',
                payment_date=timezone.now()
            )
            # Javobni tayyorlash (yangilangan ma'lumotlar bilan)
            response_serializer = PaymentSerializer(payment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)