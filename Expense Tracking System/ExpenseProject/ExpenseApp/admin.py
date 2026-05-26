from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Incomecategories)
admin.site.register(Expensescategories)
admin.site.register(income)
admin.site.register(expenses)
