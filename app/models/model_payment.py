# from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone

from .auth_users import *
# from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
class Month(BaseModel):
    MONTH_CHOICES = [
        (1, 'Yanvar'),
        (2, 'Fevral'),
        (3, 'Mart'),
        (4, 'Aprel'),
        (5, 'May'),
        (6, 'Iyun'),
        (7, 'Iyul'),
        (8, 'Avgust'),
        (9, 'Sentabr'),
        (10, 'Oktabr'),
        (11, 'Noyabr'),
        (12, 'Dekabr'),
    ]
    month_number=models.PositiveSmallIntegerField(choices=MONTH_CHOICES,validators=[MinValueValidator(1),MaxValueValidator(12)],verbose_name="oy raqami")
    year = models.PositiveIntegerField(verbose_name="yil", default=datetime.datetime.now().year)
    name=models.CharField(max_length=25,editable=False,verbose_name="oy nomi")
    start_date=models.DateField(verbose_name="boshlanish sanasi")
    end_date=models.DateField(verbose_name="tugash vaqti")
    description=models.TextField(blank=True,null=True,verbose_name="qoshimcha malumot")
    class Meta:
        verbose_name="oy"
        verbose_name_plural="oylar"
        unique_together = ('month_number', 'year')  # Bir yilda bir oy bir marta
        ordering = ['year', 'month_number']
        # Django avtomatik yaratadigan metodni qo'lda e'lon qilamiz

    def get_month_number_display(self):
        """Return the display name for the month_number field."""
        return dict(self.MONTH_CHOICES).get(self.month_number, str(self.month_number))

    def __str__(self):
        return f"{self.get_month_number_display()} {self.year}"

    def save(self, *args, **kwargs):
        # Avtomatik ravishda oy nomini to'ldirish
        self.name = self.get_month_number_display()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Oyning davomiyligi (kunlarda)"""
        return (self.end_date - self.start_date).days + 1




class Payment(BaseModel):
    PAYMENT_STATUS_CHOICES = [
        ('paid', "To'langan"),
        ('unpaid', "To'lanmagan"),
        ('partial', "Qisman to'langan"),
        ('cancelled', "Bekor qilingan"),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', "Naqd pul"),
        ('card', "Bank kartasi"),
        ('transfer', "Bank o'tkazmasi"),
        ('click', "Click"),
        ('payme', "Payme"),
    ]


    student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey('GroupStudent', on_delete=models.CASCADE, related_name='payments')
    month = models.ForeignKey('Month', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="To'lov miqdori")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    payment_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "To'lov"
        verbose_name_plural = "To'lovlar"
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.student} - {self.amount} ({self.get_status_display()})"


