from ..models import GroupStudent
from ..models.model_attendance import *
from rest_framework import serializers
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=['group','date','descriptions']


# StudentAttendance uchun alohida serializer
class StudentAttendanceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = ['id', 'attendance', 'student', 'status']
        depth = 1  # Bog'langan obyektlarni ham ko'rsatish


class AttendanceCreateSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=GroupStudent.objects.all())
    date = serializers.DateField()
    descriptions = serializers.CharField(required=False, allow_blank=True)

    # Talabalar IDsi va ularning statuslari uchun dictionary
    # Namuna: {"1": "bor", "2": "yo'q", "3": "kechikkan"}
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
    )

    def validate(self, data):
        """Tekshirishlar"""
        group = data['group']
        student_ids = data['attendances'].keys()

        # Talabalar ushbu guruhda borligini tekshiramiz
        students_in_group = group.get_group.filter(id__in=student_ids).count()
        if students_in_group != len(student_ids):
            raise serializers.ValidationError("Ba'zi talabalar bu guruhga tegishli emas")

        return data

    def create(self, validated_data):
        """Attendance va StudentAttendance'larni yaratish"""
        group = validated_data['group']
        date = validated_data['date']
        descriptions = validated_data.get('descriptions', '')
        attendances_data = validated_data['attendances']

        # 1. Yangi Attendance yaratamiz
        attendance = Attendance.objects.create(
            group=group,
            date=date,
            descriptions=descriptions
        )

        # 2. Har bir talaba uchun StudentAttendance yaratamiz
        student_attendances = []
        for student_id, status in attendances_data.items():
            student_attendances.append(
                StudentAttendance(
                    attendance=attendance,
                    student_id=student_id,
                    status=status
                )
            )

        StudentAttendance.objects.bulk_create(student_attendances)

        return attendance
