from ..models.model_homework import *
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied


class HomeWorkSerializer(serializers.ModelSerializer):
    fayl = serializers.FileField(required=False, allow_null=True)  # Fayl optional, Swaggerda to‘g‘ri ko‘rinadi
    class Meta:
        model = Homework
        fields = ['id', 'sarlavha', 'group', 'teacher', 'topshirish_muddati', 'fayl']
        read_only_fields = ['holati']  # Holat avtomatik yangilanadi

        def validate(self, attrs):
            request = self.context.get('request')
            student = attrs.get('student')
            teacher = request.user
            group = getattr(student, 'group', None)

            if not group:
                raise PermissionDenied("Talabaning guruhi yo‘q.")

            if hasattr(group.teacher, 'all'):
                if teacher not in group.teacher.all():
                    raise PermissionDenied("Siz bu guruhdagi studentga homework yozolmaysiz.")
            elif group.teacher != teacher:
                raise PermissionDenied("Siz bu guruhdagi studentga homework yozolmaysiz.")

            return attrs


class BaholashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topshiriq
        fields = ['id', 'baho', 'sharh']
        read_only_fields = ['homework', 'student', 'javob', 'ilova', 'topshirilgan_sana']

class TopshirishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topshiriq
        fields=['id','homework','student','javob','ilova']
        read_only_fields = ['topshirilgan_sana', 'baho', 'sharh'] #bu qator faqat get qilganda ko'rinadi post vaputda chiqmaydi
