from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class income(models.Model):
    IncomeCategory = models.CharField(max_length=30)
    IncomeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    IncomeDescription = models.TextField(blank=True, null=True)
    IncomeDate = models.DateField()

    def __str__(self):
         return f"{self.IncomeCategory} : {self.IncomeAmount}"


class expenses(models.Model):
    ExpensesCategory = models.CharField(max_length=30)
    ExpensesAmount = models.DecimalField(max_digits=10, decimal_places=2)
    ExpensesDescription = models.TextField(blank=True, null=True)
    ExpensesDate = models.DateField()

    def __str__(self):
        return f"{self.ExpensesCategory} : {self.ExpensesAmount}"


class totals(models.Model):
    TotalIncome = models.DecimalField(max_digits=10, decimal_places=2)
    TotalExpenses = models.DecimalField(max_digits=10, decimal_places=2)
    LatestTotalInc_As_of = models.DateField()
    LatestTotalExp_As_of = models.DateField()

    def __str__(self):
        return f"Total Income Amount {self.TotalIncome} : Total Expenses Amount {self.TotalExpenses}"

