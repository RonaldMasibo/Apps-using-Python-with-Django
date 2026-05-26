from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Incomecategories(models.Model):
    forIncome = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.forIncome} is a category for income"


class income(models.Model):
    IncomeCategory = models.ForeignKey(
        Incomecategories, # Links to the categories model
        on_delete=models.PROTECT, # Prevents deleting a category that has generated income
    )
    IncomeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    IncomeDescription = models.TextField(blank=True, null=True)
    IncomeDate = models.DateField()

    def __str__(self):
        return f" The amount for income was : {self.IncomeAmount}"


class Expensescategories(models.Model):
    forExpenses = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.forExpenses} is a category for expenses"

class expenses(models.Model):
    ExpensesCategory = models.ForeignKey(
        Expensescategories, on_delete=models.PROTECT)
    ExpensesAmount = models.DecimalField(max_digits=10, decimal_places=2)
    ExpensesDescription = models.TextField(blank=True, null=True)
    ExpensesDate = models.DateField()
    
    def __str__(self):
        return f"{self.ExpensesCategory} : {self.ExpensesAmount}"

