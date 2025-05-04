from rest_framework import serializers

from . import CourseSerializer
from .teacher_serializers import TeacherSerializer
from ..models import Day, Rooms, TableType, Table, GroupStudent, Teacher


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class GroupStudentSerializer(serializers.ModelSerializer):
    # For foreign key relationships - display full object
    course = serializers.StringRelatedField()
    table = TableSerializer(read_only=True)

    # For many-to-many relationship with Teacher
    teacher = serializers.StringRelatedField(many=True)

    class Meta:
        model = GroupStudent
        fields = '__all__'
        extra_kwargs = {
            'start_date': {'format': '%Y-%m-%d'},
            'end_date': {'format': '%Y-%m-%d'},
        }


# If you need nested serializers for related fields:
class GroupStudentDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)  # Assuming you have CourseSerializer
    teacher = TeacherSerializer(many=True, read_only=True)  # Assuming you have TeacherSerializer
    table = TableSerializer(read_only=True)

    class Meta:
        model = GroupStudent
        fields = '__all__'




#
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupStudent
#         fields = ['title', 'course', 'teacher', 'table', 'start_date', 'end_date']


class GroupSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all(), many=True)

    class Meta:
        model = GroupStudent
        fields = '__all__'





















from rest_framework import serializers
from ..models import GroupStudent

class GroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['name']  # Faqat nomini o'zgartirish uchun

class GroupSerializerT(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'name', 'students_count']  # O'qituvchi ko'radigan maydonlar

class GroupAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = '__all__'  # Admin uchun barcha maydonlar