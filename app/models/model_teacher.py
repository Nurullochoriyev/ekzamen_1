
from .auth_users import *
# Markazda oqitiladigan fanlar
class Course(BaseModel):
    title=models.CharField(max_length=50)
    descriptions=models.CharField(max_length=500,null=True,blank=True)
    def __str__(self):
        return self.title


# Xodimlarning darajasini belgilash uchun
class Departments(BaseModel):
    title=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)
    descriptions=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.title



# Xodimlarning datalarini saqlash uchun yuqoridagi Course va Departments modellari Worker bog'langan
class Teacher(BaseModel):
    user=models.OneToOneField(User,on_delete=models.RESTRICT,related_name='user')
    departments=models.ManyToManyField(Departments ,related_name="get_department")
    course=models.ManyToManyField(Course,related_name="get_course")
    descriptions=models.CharField(max_length=500,blank=True,null=True)


    def __str__(self):
        return f"{self.user.username} ({self.user.phone_number})"