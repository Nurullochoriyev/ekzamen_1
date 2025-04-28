from rest_framework import serializers


class PaymentStatisticsSerializer(serializers.Serializer):
    total_payments = serializers.IntegerField()
    total_paid = serializers.IntegerField()
    total_unpaid = serializers.IntegerField()
    total_partial = serializers.IntegerField()
    total_cancelled = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2)



class GroupStudentStatistikaSerializer(serializers.Serializer):
    graduated_groups = serializers.IntegerField()
    studying_groups = serializers.IntegerField()
    enrolled_groups = serializers.IntegerField()

