from django.contrib.auth import authenticate
from django.db import transaction

from rest_framework import serializers
from app.models import *



class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self,attrs):
        username=attrs.get("username")
        password=attrs.get("password")
        try:
            user=User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "success":False,
                    "detail":"user doest not exist"
                }
            )
        auth_user=authenticate(username=user.username,password=password)
        if auth_user is None:
            raise serializers.ValidationError(
                {
                    "success":False,
                    "detail":"username or password is invalid"
                }

            )
        attrs["user"]=auth_user
        return attrs










#
# class TeacherCreateSerializer(serializers.ModelSerializer):
#     phone_number = serializers.CharField(write_only=True)
#     password = serializers.CharField(write_only=True)
#     full_name = serializers.CharField(write_only=True, required=False)
#
#     class Meta:
#         model = Teacher
#         fields = ['departments', 'course', 'descriptions', 'phone_number', 'password', 'full_name']
#
#     def validate_phone_number(self, value):
#         if User.objects.filter(phone_number=value).exists():
#             raise serializers.ValidationError("Ushbu telefon raqam allaqachon ro'yxatdan o'tgan")
#         return value
# # ===============================================
#     def create(self, validated_data):
#         try:
#             with transaction.atomic():
#                 # User yaratish
#                 user_data = {
#                     'phone_number': validated_data.pop('phone_number'),
#                     'password': validated_data.pop('password'),
#                     'full_name': validated_data.pop('full_name', ''),
#                     'is_teacher': True
#                 }
#
#                 user = User.objects.create_user(**user_data)
#
#                 # Teacher yaratish
#                 departments = validated_data.pop('departments', [])
#                 courses = validated_data.pop('course', [])
#
#                 teacher = Teacher.objects.create(user=user, **validated_data)
#
#                 # ManyToMany maydonlarini sozlash
#                 teacher.departments.set(departments)
#                 teacher.course.set(courses)
#
#                 return teacher
#
#         except Exception as e:
#             raise serializers.ValidationError(str(e))
#
#
#
# # ========================================
#
#
#
#
#
#
#



from rest_framework import serializers
from ..models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
        'id', 'phone_number', 'password','email', 'is_active', 'is_staff', "is_teacher", 'is_admin', 'is_student')


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.check_password(
                validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 're_new_password']


class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'descriptions']


class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'title', 'is_active', 'descriptions']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", 'user', 'departments', 'course', 'descriptions']




class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = ['id', 'title', 'descriptions']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudent
        fields = ['id', 'title', 'course', 'teacher', "table", 'start_date', 'end_date', 'price', 'descriptions']


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['id', 'title', 'descriptions']


class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ['id', 'title', 'descriptions']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']


    # class StudentSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = Student
    #         fields = [ 'user', 'group',  'is_line', 'descriptions']
    #
    # #
# #
# class TopicsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Topics
#         fields = ['id', 'title', 'course', 'descriptions']
#
#
# class GroupHomeWorkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GroupHomeWork
#         fields = ['id', 'group', 'topic', 'is_active', 'descriptions']
#
#
# class HomeWorkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HomeWork
#         fields = ['id', 'groupHomeWork', 'price', 'student', 'link', 'is_active', 'descriptions']
#
#
# class AttendanceLevelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AttendanceLevel
#         fields = ['id', 'title', 'descriptions']