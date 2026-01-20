from django.db import models

# Create your models here.


class RegisteredUsersModel(models.Model):
    First_Name = models.CharField(max_length=100, blank=False, null=False)
    Middle_Name = models.CharField(max_length=100, blank=False, null=True)
    Last_Name = models.CharField(max_length=100, blank=False, null=False)
    Email = models.EmailField( unique=True, max_length=50, blank=False, null=False)
    Password = models.CharField(max_length=100)

    def __str__(self):
        return self.First_Name
