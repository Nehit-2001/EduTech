from django.db import models

# Create your models here.
class Signup(models.Model):
    first_name = models.CharField(max_length=100, null=True, default="")
    last_name = models.CharField(max_length=100, null=True, default="")
    email = models.CharField(max_length=100, null=True, default="")
    password = models.CharField(max_length=255, null=True, default="")
    mobile = models.BigIntegerField(null=True)
    gender = models.CharField(max_length=100, null=True, default="")
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    

class Course_details(models.Model):
    course_name = models.CharField(max_length=100, null=True, default="")
    slug = models.CharField(max_length=100, null=True, default="")
    desc = models.TextField(max_length=200, null=True, default="")
    price = models.IntegerField(null=True, default=1)
    discount= models.IntegerField(null=True, default=1)
    course_image = models.ImageField(upload_to='static/images/')
    resource = models.FileField(upload_to='resources/course/')
    duration = models.TimeField()
    
    def __str__(self):
        return self.course_name
    

class Videos(models.Model):
    video_title = models.CharField(max_length=100, blank=True, null=True)
    video_id = models.CharField(max_length=100, blank=True, null=True)
    video_belong = models.ForeignKey(Course_details, on_delete=models.CASCADE, default=1)
    video_seq = models.IntegerField(null=True, blank=True)
    is_preview = models.BooleanField(default=False)
    
    def __str__(self):
        return self.video_title
    

class Course_info(models.Model):
    desc = models.CharField(max_length=100, null=True, blank=True)
    course = models.ForeignKey(Course_details, on_delete=models.CASCADE)
    
    class Meta:
        abstract = True


class tag(Course_info):
    pass


class prereq(Course_info):
    pass


class learning(Course_info):
    pass
    
    
class User_Course(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_details, on_delete=models.CASCADE) 
    
    def __str__(self):
        return f'{self.user.first_name} - {self.course.course_name}'
    

class Payment(models.Model):
    order_id = models.CharField(max_length=200, null=True, blank=True)
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    user_info = models.ForeignKey(Signup, on_delete=models.CASCADE)
    course = models.ForeignKey(Course_details, on_delete=models.CASCADE)
    course_info = models.ForeignKey(User_Course, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.order_id
    

class Ref_code(models.Model):
    code = models.CharField(max_length=100)
    course = models.ForeignKey(Course_details, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)
    
    def __str_(self):
        return self.code
    