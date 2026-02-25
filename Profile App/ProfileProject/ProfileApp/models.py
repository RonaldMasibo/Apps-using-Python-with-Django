from django.db import models

# Create your models here.


class People(models.Model):
    f_name = models.CharField(max_length=40)
    m_name = models.CharField(max_length=40)
    l_name = models.CharField(max_length=40)
    prof_img = models.ImageField(upload_to="media/")
    phone_no = models.CharField(max_length=13)

    def __str__(self):
        return f"Welcome {self.f_name} to your app for storing different profiles!!!"