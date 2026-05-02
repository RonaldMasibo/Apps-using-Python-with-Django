from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class IncomeCategories(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"Category {self.title}"

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategories, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} : {self.income}"
    
    # staticmethod declares a method that does not depend on a specific instance
    @staticmethod
    # the function below gets the total income for a specific user
    def get_total_income(user):
        return Income.objects.filter(user=user).aggregate(total=models.Sum('income'))['total'] or 0
    


class ExpensesCategories(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return f"Total: {self.TotalExpenses}"

class Expenses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpensesCategories, on_delete=models.CASCADE)
    expenses = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category} : {self.expenses}"

    # staticmethod declares a method that does not depend on a specific instance
    @staticmethod
    # the function below gets the total expenses for a specific user
    def get_total_expenses(user):
        """
            .aggregate(....) -> calculates the sum of all amounts
            ['total] or 0 -> Extracts the total value. If there's no data, it returns 0
        """
        return Expenses.objects.filter(user=user).aggregate(total=models.Sum('expenses'))['total'] or 0
        


"""
    Helper methods to get category totals
"""
def get_income_by_category(user):
    # Function that groups income by category
    """
        .values('category_title') -> Group by category title
        .annotate(....) -> Sum per category
        .order_by('-total) -> sort by descending
    """
    return (
        Income.objects.filter(user=user).values('category_title').annotate(total=models.Sum('income')).order_by('-total')
    )

def get_expenses_by_category(user):
    return (
        Expenses.objects.filter(user=user).values('category_title').annotate(total=models.Sum('expenses')).order_by('-total')
    )