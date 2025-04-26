from rest_framework import serializers

from . import UserSerializer
# from ..models import GroupStudent, Student
from ..models.model_teacher import  *
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=["id","user","departments","course","descriptions"]










class TeacherUserSerializer(serializers.ModelSerializer):
    is_active=serializers.BooleanField(read_only=True)
    is_teacher=serializers.BooleanField(read_only=True)
    is_student=serializers.BooleanField(read_only=True)
    is_staff=serializers.BooleanField(read_only=True)
    is_admin=serializers.BooleanField(read_only=True)
    class Meta:
        abstract=True
        model=User
        fields=('id','phone_number','password','email','is_active', 'is_teacher', 'is_student', 'is_staff','is_admin')
class TeacherPostSerializer(serializers.Serializer):
    user = TeacherUserSerializer()
    id = serializers.IntegerField(read_only=True)
    departments = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(),many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),many=True)
    class Meta:
        model = Teacher
        fields = ["id","user","departments","course","descriptions"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        user_db["is_active"] = True
        user_db["is_teacher"] = True
        departments_db = validated_data.pop("departments")
        course_db = validated_data.pop("course")
        user = User.objects.create_user(**user_db)
        teacher = Teacher.objects.create(user=user,**validated_data)
        teacher.departments.set(departments_db)
        teacher.course.set(course_db)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        departments = validated_data.pop("departments", None)
        courses = validated_data.pop("course", None)

        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if departments is not None:
            instance.departments.set(departments)

        if courses is not None:
            instance.course.set(courses)

        instance.save()
        return instance

class TeacherUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    user = TeacherUserSerializer(required=False)  # nested user update

    class Meta:
        model = Teacher
        fields = ["id", "user", "departments", "course", "descriptions"]
        extra_kwargs = {
            "id": {"required": True},
            "departments": {"required": False},
            "course": {"required": False},
            "descriptions": {"required": False}
        }

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        departments = validated_data.pop("departments", None)
        courses = validated_data.pop("course", None)

        # User (nested) yangilash
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        # Teacher modeldagi qolgan maydonlar
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if departments is not None:
            instance.departments.set(departments)

        if courses is not None:
            instance.course.set(courses)

        instance.save()
        return instance
