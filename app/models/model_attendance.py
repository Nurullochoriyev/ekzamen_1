from django.db import models
from django.utils import timezone


class Attendance(models.Model):
    group = models.ForeignKey('GroupStudent', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    descriptions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.group.title} - {self.date}"


class TAttendance(models.Model):

    date = models.DateField(default=timezone.now)
    descriptions = models.TextField(blank=True)
    def __str__(self):
        return self.date

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

    def __str__(self):
        return self.student.user.username

class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('bor', "Bor"),
        ("yo'q", "Yo'q"),
        ("kechikkan", "Kechikkan"),
        ("sababli", "Sababli")
    ]
    attendance = models.ForeignKey(TAttendance, on_delete=models.CASCADE, related_name='teacher_attendances')
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        verbose_name = "O'qituvchi davomadi"
        verbose_name_plural = "O'qituvchilar davomadi"
        unique_together = ['attendance','teacher']  # Bir kunga bir marta yozilishi

    def __str__(self):
        return self.teacher.user.username







