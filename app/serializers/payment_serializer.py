from ..models.model_payment import *
from rest_framework import serializers
class MonthSerializer(serializers.ModelSerializer):

    class Meta:
        model=Month
        fields=['month_number','year','name','start_date','end_date','description']

class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(
        choices=[('cash', 'Naqd pul'), ('card', 'Bank kartasi'),
                 ('transfer', "Bank o'tkazmasi"), ('click', 'Click'),
                 ('payme', 'Payme')],
        default='cash'
    )
    class Meta:
        model=Payment
        fields=['student','group','month','amount','status','payment_method','description','payment_date']
        read_only_fields=['status']



