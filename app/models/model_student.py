
from .model_teacher import *
class Student(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    group=models.ManyToManyField('GroupStudent',related_name='get_group')

    is_line=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    descriptions=models.CharField(max_length=500,blank=True,null=True)
    def __str__(self):
        return self.user.phone



class Parents(BaseModel):
    student=models.OneToOneField(Student,on_delete=models.CASCADE,related_name='get_student')
    full_name=models.CharField(max_length=50,null=True,blank=True)
    phone_number=models.CharField(max_length=15,null=True,blank=True)
    address=models.CharField(max_length=200,null=True,blank=True)
    descriptions=models.CharField(max_length=500,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.full_name