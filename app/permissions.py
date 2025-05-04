
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrTeacherLimitedEdit(BasePermission):
    """
    Admin: to‘liq CRUD
    Teacher: faqat PUT/PATCH (title o‘zgartirish)
    """

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (user.is_admin or user.is_teacher)

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin: to‘liq ruxsat
        if user.is_admin:
            return True

        # Teacher: faqat PATCH va faqat 'title' ni o‘zgartirsa bo‘ladi  + GET
        if user.is_teacher and request.method in ['PATCH', 'PUT','GET']:
            allowed_fields = {'title'}
            incoming_fields = set(request.data.keys())

            return incoming_fields.issubset(allowed_fields)

        return False






from rest_framework import permissions
# teacher uchun ruhsatlar
class IsTeacher(permissions.BasePermission):
    message = "Faqat o'qituvchilar uchun ruxsat berilgan"

    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'is_teacher') and request.user.is_teacher




from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'is_admin'


# Staff bo‘lsa, CRUD qilish huquqini beramiz.
class IsStaffUser(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and request.user.is_authenticated and request.user.is_staff)




from rest_framework.permissions import BasePermission

class IsTeacherOfStudentPermission(BasePermission):
    """
    Teacher faqat o‘z guruhidagi studentga ishlov bera oladi.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_teacher

    def has_object_permission(self, request, view, obj):
        student = getattr(obj, 'student', None)
        group = getattr(student, 'group', None)

        if not group:
            return False

        teacher = request.user

        # ManyToMany bo‘lsa
        if hasattr(group.teacher, 'all'):
            return teacher in group.teacher.all()

        # ForeignKey bo‘lsa
        return group.teacher == teacher
