from django.db import models

class Attendance(models.Model):
    group = models.ForeignKey('GroupStudent', on_delete=models.CASCADE)
    date = models.DateField()
    descriptions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.group.name} - {self.date}"

class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('bor', "Bor"),
        ("yo'q", "Yo'q"),
        ("kechikkan", "Kechikkan"),
        ("sababli","Sabali")
    ]
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='student_attendances')
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('bor', "Bor"),
        ("yo'q", "Yo'q"),
        ("kechikkan", "Kechikkan"),
        ("sababli", "Sabali")
    ]
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='teacher_attendances')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)




























# from rest_framework.utils import timezone
#
# from ..models import *
# from django.utils import timezone
#
# class Level(BaseModel):
#     title = models.CharField(max_length=200)
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#
#     def __str__(self):
#         return self.title
#
#
# class Attendance(BaseModel):
#
#     teacher = models.ForeignKey(User,on_delete=models.PROTECT,related_name='marked_attendances'
#         )
#
#     student = models.ForeignKey(Student, on_delete=models.RESTRICT, related_name='get_students')
#     group = models.ForeignKey(GroupStudent, on_delete=models.RESTRICT, related_name='get_group_student')
#     descriptions = models.CharField(max_length=500, blank=True, null=True)
#     date = models.DateField(
#         verbose_name="Sana",
#         default=timezone.now,
#         help_text="Davomat sanasi"
#     )
#     status = models.CharField(
#         max_length=20,
#         choices=[('present', 'Present'),('absent', 'Absent'),('late', 'Late'),('excused', 'Excused'),
#         ],
#         default='present',
#         verbose_name="Holati"
#     )
#     check_in = models.TimeField(
#         null=True,
#         blank=True,
#         verbose_name="Kelish vaqti"
#     )
#     check_out = models.TimeField(
#         null=True,
#         blank=True,
#         verbose_name="Ketish vaqti"
#     )
#
#     is_active = models.BooleanField(
#         default=True,
#         verbose_name="Faol"
#     )
#
#     class Meta:
#         verbose_name = "Davomat"
#         verbose_name_plural = "Davomatlar"
#         unique_together = ('student', 'date')  # Har bir talaba uchun kuniga 1 davomat
#         ordering = ['-date', 'student']
#
#     def __str__(self):
#         return f"{self.student} - {self.date} - {self.status}"
