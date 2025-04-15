from rest_framework import serializers

from . import UserSerializer
from ..models import Parents, Student, GroupStudent
from ..models.model_teacher import  *
class StudentSerializer(serializers.ModelSerializer):
    # group= serializers.PrimaryKeyRelatedField(queryset=GroupStudent.objects.all(),many=True)
    class Meta:
        model=Student

        fields=["user","group","is_line","descriptions"]
    # def create(self, validated_data):
    #     user_db=validated_data.pop("user")
    #     group_db=validated_data.pop("group")
    #     user=User.objects.create_user(**user_db)
    #     student=Student.objects.create(user=user,**validated_data)
    #     student.group.set(group_db)
    #     return student



class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parents
        fields=["full_name","phone_number","address","descriptions"]
class GroupStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=GroupStudent
        fields=['title','course','table','start_date','end_date','descriptions']


class StudentUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    class Meta:
        abstract=True
        model=User
        fields=('id','phone_number','password','email','is_active', 'is_teacher', 'is_student', 'is_staff','is_admin')
class StudentSerializerPost(serializers.Serializer):
    user=StudentUserSerializer()
    student=StudentSerializer()
    # parents=ParentsSerializer()
    # group_student=GroupStudentSerializer()





