from ..models import GroupStudent, Teacher
from ..models.model_attendance import *
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attendance
        fields=['group','date','descriptions']

        def validate(self, attrs):
            request = self.context.get('request')
            student = attrs.get('student')
            teacher = request.user
            group = getattr(student, 'group', None)

            if not group:
                raise PermissionDenied("Talabaning guruhi yo‘q.")

            if hasattr(group.teacher, 'all'):
                if teacher not in group.teacher.all():
                    raise PermissionDenied("Siz bu guruhdagi studentga attendance yozolmaysiz.")
            elif group.teacher != teacher:
                raise PermissionDenied("Siz bu guruhdagi studentga attendance yozolmaysiz.")

            return attrs


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

    def update(self, instance, validated_data):
        """Attendance va unga bog'langan StudentAttendance'larni yangilash"""
        instance.date = validated_data.get('date', instance.date)
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)
        instance.save()

        attendances_data = validated_data.get('attendances', {})

        # Eski student attendance yozuvlarini tozalaymiz
        instance.student_attendances.all().delete()  # ← to‘g‘ri related_name bilan

        # Yangilangan attendances asosida yangi yozuvlar yaratamiz
        student_attendances = []
        for student_id, status in attendances_data.items():
            student_attendances.append(
                StudentAttendance(
                    attendance=instance,
                    student_id=student_id,
                    status=status
                )
            )

        StudentAttendance.objects.bulk_create(student_attendances)

        return instance


# class TAttendanceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=TAttendance
#         fields=['date','descriptions']
class TeacherAttendanceBulkSerializer(serializers.Serializer):
    date = serializers.DateField(default=timezone.now)
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
    )
    descriptions = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        teacher_ids = [str(id) for id in data['attendances'].keys()]
        existing_teachers = Teacher.objects.filter(id__in=teacher_ids).count()
        if existing_teachers != len(teacher_ids):
            raise serializers.ValidationError("Ba'zi IDlarga mos o'qituvchilar topilmadi")
        return data

    def create(self, validated_data):
        date = validated_data['date']
        attendances_data = validated_data['attendances']
        descriptions = validated_data.get('descriptions', '')

        t_attendance = TAttendance.objects.create(
            date=date,
            descriptions=descriptions
        )

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

    def update(self, instance, validated_data):
        """
        TAttendance va unga bog'langan TeacherAttendance'larni yangilash
        """
        # Asosiy TAttendance ni yangilash
        instance.date = validated_data.get('date', instance.date)
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)
        instance.save()

        # Yangi attendances ma'lumotlari
        new_attendances = validated_data.get('attendances', {})

        # Mavjud TeacherAttendance'larni olish
        existing_attendances = {
            str(ta.teacher_id): ta for ta in instance.teacher_attendances.all()
        }

        # Yangilash yoki yaratish uchun list
        to_update = []
        to_create = []

        for teacher_id, status in new_attendances.items():
            if teacher_id in existing_attendances:
                # Mavjud bo'lsa yangilash
                ta = existing_attendances[teacher_id]
                ta.status = status
                to_update.append(ta)
            else:
                # Yangi yaratish
                to_create.append(
                    TeacherAttendance(
                        attendance=instance,
                        teacher_id=teacher_id,
                        status=status
                    )
                )

        # Bulk update qilish
        if to_update:
            TeacherAttendance.objects.bulk_update(to_update, ['status'])

        # Bulk create qilish
        if to_create:
            TeacherAttendance.objects.bulk_create(to_create)

        return instance
#################################################
from rest_framework import serializers

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher  # model nomi sizda qanday bo‘lsa
        fields = ['id', 'user']  # yoki kerakli maydonlar

class TAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TAttendance
        fields = ['id', 'date', 'descriptions']

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    teacher = TeacherSerializer()
    attendance = TAttendanceSerializer()

    class Meta:
        model = TeacherAttendance
        fields = ['id', 'teacher', 'attendance', 'status']
























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
