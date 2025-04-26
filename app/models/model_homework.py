from django.utils import timezone

from .model_teacher import *

from django.db import models

from . import GroupStudent, Student
from .auth_users import*
class Homework(BaseModel):
    HOLAT_TANLOV = [
        ('faol', 'Faol'),
        ('muddati_utgan', 'Muddati o`tgan'),
        ('arxiv', 'Arxivlangan'),
    ]
    sarlavha=models.CharField(max_length=200,verbose_name='vazifa sarlavhasi')
    group=models.ForeignKey(GroupStudent,on_delete=models.CASCADE,related_name='get_home_groupstudent')
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE,related_name='get_home_teacher')
    topshirish_muddati = models.DateTimeField(verbose_name="Topshirish sanasi")
    holati = models.CharField(max_length=15, choices=HOLAT_TANLOV, default='faol')
    fayl = models.FileField(upload_to='uy_vazifalari/', blank=True, null=True, verbose_name="Vazifa fayli")

    def saqlash(self, *args, **kwargs):
        if self.topshirish_muddati < timezone.now():
            self.holati = 'muddati_utgan'
        super().saqlash(*args, **kwargs)

    def __str__(self):
        return f"{self.sarlavha} ({self.group.title})"

    class Meta:
        verbose_name = "Uy vazifasi"
        verbose_name_plural = "Uy vazifalari"
        ordering = ['-created_ed']


class Topshiriq(BaseModel):
    BAHO_TANLOV = [
        (0, 'Baholanmagan'),
        (1, 'Qoniqarsiz'),
        (2, 'Qoniqarli'),
        (3, 'Yaxshi'),
        (4, 'A`lo'),
        (5, 'Mukammal'),
    ]

    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='topshiriqlar')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Topshiruvchi talaba")
    topshirilgan_sana = models.DateTimeField(auto_now_add=True)
    javob = models.TextField(verbose_name="Talaba javobi")
    ilova = models.FileField(upload_to='topshiriqlar/', blank=True, null=True)
    baho = models.IntegerField(choices=BAHO_TANLOV, default=0, verbose_name="Topshiriq bahosi")
    sharh = models.TextField(blank=True, verbose_name="O'qituvchi sharhi")

    def __str__(self):
        return f"{self.student.user.username} - {self.homework.sarlavha}"

    class Meta:
        verbose_name = "Topshiriq"
        verbose_name_plural = "Topshiriqlar"
        unique_together = ['homework', 'student']  # Har bir talaba bitta vazifaga bir marta javob berishi mumkin