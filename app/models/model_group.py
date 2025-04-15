




from app.models import BaseModel
from .model_teacher import *
from ..models import *

class Day (models.Model):
    title=models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return  self.title

class Rooms(BaseModel):
    title=models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.title


class TableType(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.title

class Table(BaseModel):
    start_time=models.TimeField()
    end_time=models.TimeField()
    room=models.ForeignKey(Rooms,on_delete=models.RESTRICT)
    type=models.ForeignKey(TableType,on_delete=models.RESTRICT)
    descriptions = models.CharField(max_length=500, null=True, blank=True)


class GroupStudent(BaseModel):
    title=models.CharField(max_length=25,unique=True)
    course=models.ForeignKey(Course, on_delete=models.RESTRICT,related_name='course')
    teacher=models.ManyToManyField(Teacher,related_name="get_teacher")
    table=models.ForeignKey(Table,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.title

