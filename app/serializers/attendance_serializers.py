from ..models import GroupStudent, Teacher
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


class TAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=TAttendance
        fields=['date','descriptions']

class TeacherAttendanceBulkSerializer(serializers.Serializer):
    date = serializers.DateField(default=timezone.now)
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
    )
    descriptions = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        teacher_ids = [str(id) for id in data['attendances'].keys()]  # Stringga o'tkazamiz
        existing_teachers = Teacher.objects.filter(id__in=teacher_ids).count()
        if existing_teachers != len(teacher_ids):
            raise serializers.ValidationError("Ba'zi IDlarga mos o'qituvchilar topilmadi")
        return data

    def create(self, validated_data):
        date = validated_data['date']
        attendances_data = validated_data['attendances']
        descriptions = validated_data.get('descriptions', '')

        # TAttendance yaratamiz
        t_attendance = TAttendance.objects.create(
            date=date,
            descriptions=descriptions
        )

        # Har bir o'qituvchi uchun TeacherAttendance yaratamiz
        teacher_attendances = []
        for teacher_id, status in attendances_data.items():
            teacher_attendances.append(
                TeacherAttendance(
                    attendance=t_attendance,
                    teacher_id=teacher_id,
                    status=status
                )
            )

        TeacherAttendance.objects.bulk_create(teacher_attendances)
        return t_attendance





























# class TeacherAttendanceSerializer(serializers.Serializer):
#     # Talabalar IDsi va ularning statuslari uchun dictionary
#     # Namuna: {"1": "bor", "2": "yo'q", "3": "kechikkan"}
#     teacher=serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
#     date = serializers.DateField(default=timezone.now)
#     attendances = serializers.DictField(
#         child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
#     )
#     descriptions = serializers.CharField(blank=True)
#
#     def validate(self, data):
#         teacher = data['teacher']
#         teacher_ids = data['attendances'].keys()
#         teachers_in_group = teacher.get_users.filter(id__in=teacher_ids).count()
#         if teachers_in_group != len(teacher_ids):
#             raise serializers.ValidationError("Ba'zi foydalanuvchi teacher emas")
#         return data
#
#     def create(self,validated_data):
#         # teacher=validated_data['teacher'],
#         date=validated_data['date'],
#         attendances=validated_data['attendance'],
#         descriptions=validated_data['descriptions']
#         attendance=Attendance.objects.create(
#
#             date=date,
#
#             descriptions=descriptions,
#
#         )
#         teacher_attendance=[]
#         for teacher_id, status in attendances.items():
#             teacher_attendance.append(
#                 TeacherAttendance(
#                 attendance=attendance,
#                 teacher_id=teacher_id,
#                 status=status)
#             )
#         TeacherAttendance.objects.bulk_create(teacher_attendance)
#         return attendance
#
#
