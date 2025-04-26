from ..models.model_homework import *
from rest_framework import serializers


class HomeWorkSerializer(serializers.ModelSerializer):
    fayl = serializers.FileField(required=False, allow_null=True)  # Fayl optional, Swaggerda to‘g‘ri ko‘rinadi
    class Meta:
        model = Homework
        fields = ['id', 'sarlavha', 'group', 'teacher', 'topshirish_muddati', 'fayl']
        read_only_fields = ['holati']  # Holat avtomatik yangilanadi




class TopshirishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topshiriq
        fields=['id','homework','student','javob','ilova']
        read_only_fields = ['topshirilgan_sana', 'baho', 'sharh'] #bu qator faqat get qilganda ko'rinadi post vaputda chiqmaydi
