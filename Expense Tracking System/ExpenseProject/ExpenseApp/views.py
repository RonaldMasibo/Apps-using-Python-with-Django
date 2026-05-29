
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import * # Importing ALL the models
from django.db.models import Sum, Count, Avg, Max, Min # For calculating the total values needed

# For generating charts
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json



# Create your views here.

def index(request):
    if request.method == 'POST':
        UserName = request.POST['Uname']
        FirstName = request.POST['Fname']
        LastName = request.POST['Lname']
        Email = request.POST['Email']
        Password = request.POST['Password1']
        Password2 = request.POST['Password2']

        if Password == Password2:
            if User.objects.filter(username = UserName).exists():
                messages.info(request, 'Username is already in use!!')
                return redirect('')
            elif User.objects.filter(email = Email).exists():
                messages.info(request, 'Email is already in use!!')
                return redirect('')
            else:
                user = User.objects.create_user(
                    username = UserName,
                    first_name = FirstName,
                    last_name = LastName,
                    email = Email,
                    password = Password
                )
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Passwords do NOT match!!')
            return redirect('')
    else:
        return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        Email = request.POST['Email']
        Password = request.POST['Password']

        user = auth.authenticate(
            email = Email,
            password = Password
        )

        if user is not None:
            auth.login(request, user)
            return redirect('calculating')
        else:
            messages.info(request, 'INVALID details!!')
            return redirect('login')
    else:
        return render(request, 'login.html')

# @login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

# @login_required
def calculating(request):

    # For the charts
    current_yr = timezone.now().year
    selected_yr = None
    expensesChart_labels = []
    expensesChart_data = []
    incomeChart_labels = []
    incomeChart_data = []
    error = None
    
    month_names = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
        'Sep', 'Oct', 'Nov', 'Dec'
    ]

    # Populate dropdown menu with the years that have Income and Expenses
    availableIncomeYears = income.objects.dates('IncomeDate', 'year', order='DESC')
    availableExpensesYears = expenses.objects.dates('ExpensesDate', 'year', order='DESC')

    if request.method == 'POST':
        # Adding an income category
        if "add_income_category" in request.POST:
            incomeCategory = request.POST.get('Income_category')

            # Adding income category to database
            incomeCategoryDetails = Incomecategories.objects.create(
                forIncome = incomeCategory
            )
            incomeCategoryDetails.save()

        # Editing an income category
        if "edit_income_category" in request.POST:
            # Get the ID of the income category first
            incomeCategory_ID = request.POST.get("incomeCategory_ID")

            # Get the details of the updated income category details
            newIncomeCategory = request.POST.get("new_IncomeCategory")

            # Fetch the object related to the passed ID and save it
            obj = get_object_or_404(Incomecategories, id = incomeCategory_ID)
            obj.save()
        
        # Deleting an income category
        if "delete_income_category" in request.POST:
            # Get the ID of the income category first
            incomeCategory_ID = request.POST.get("incomeCategory_ID")

            # Fetch the object related to the passed ID and delete it
            obj = get_object_or_404(Incomecategories, id = incomeCategory_ID)
            obj.delete()
        
        # Adding an Expense category
        if "add_expenses_category" in request.POST:
            expensesCategory = request.POST.get('Expense_category')

            # Adding expense category to database
            expensesCategoryDetails = Expensescategories.objects.create(
                forExpenses = expensesCategory
            )
            expensesCategoryDetails.save()

        # Editing an Expense category
        if "edit_expense_category" in request.POST:
            # Get the ID of the expense category first
            expenseCategory_ID = request.POST.get("expenseCategory_ID")

            # Get the details of the updated expense category details
            newExpenseCategory = request.POST.get("new_ExpenseCategory")

            # Fetch the object related to the passed ID and save it
            obj = get_object_or_404(Expensescategories, id = expenseCategory_ID)
            obj.save()
        
        # Deleting an expense category
        if "delete_expense_category" in request.POST:
            # Get the ID of the expense category first
            expenseCategory_ID = request.POST.get("expenseCategory_ID")

            # Fetch the object related to the passed ID and delete it
            obj = get_object_or_404(Expensescategories, id = expenseCategory_ID)
            obj.delete()
        
        # Adding Income
        if "add_income" in request.POST:
            # Get fields for Income
            incomeAmount = request.POST.get('Income_amount')
            incomeDescription = request.POST.get('Income_description')
            incomeDate = request.POST.get('Income_date')

            # Adding income to the database
            incomeDetails = income.objects.create(
                IncomeAmount = incomeAmount,
                IncomeDescription = incomeDescription,
                IncomeDate = incomeDate,
            )
            incomeDetails.save()

        # Editing Income Info
        if "edit_income" in request.POST:

            # Get the ID of the income first
            income_ID = request.POST.get("income_ID")

            # Get the details of the updated income details
            newIncomeAmount = request.POST.get("new_IncomeAmount")
            newIncomeDescription = request.POST.get("new_IncomeDescription")
            newIncomeDate = request.POST.get("new_IncomeDate")

            # Fetch the object related to the passed ID
            obj = get_object_or_404(income, id = income_ID)

            # Saving edited Income info
            obj.IncomeAmount = newIncomeAmount
            obj.IncomeDescription = newIncomeDescription
            obj.IncomeDate = newIncomeDate
            obj.save()

        # Deleting an Income
        if "delete_income" in request.POST:

            # Get the ID of the income first
            income_ID = request.POST.get("income_ID")

            # Fetch the object related to the passed ID and delete it
            obj = get_object_or_404(income, id = income_ID)
            obj.delete()
        
        # Adding Expenses
        if "add_expense" in request.POST:
            # Get fields for Expenses
            expensesAmount = request.POST.get('Expenses_amount')
            expensesDescription = request.POST.get('Expenses_description')
            expensesDate = request.POST.get('Expenses_date')

            # Adding expenses to the database
            expensesDetails = expenses.objects.create(
                ExpensesAmount = expensesAmount,
                ExpensesDescription = expensesDescription,
                ExpensesDate = expensesDate
            )
            expensesDetails.save()

        # Editing Expenses Info
        if "edit_expense" in request.POST:

            # Get the ID of the income first
            expenses_ID = request.POST.get("expense_ID")

            # Get the details of the updated income details
            newExpenseAmount = request.POST.get("new_ExpenseAmount")
            newExpenseDescription = request.POST.get("new_ExpenseDescription")
            newExpenseDate = request.POST.get("new_ExpenseDate")

            # Fetch the object related to the passed ID
            obj = get_object_or_404(expenses, id = expenses_ID)

            # Saving edited Income info
            obj.ExpensesAmount = newExpenseAmount
            obj.ExpensesDescription = newExpenseDescription
            obj.ExpensesDate = newExpenseDate
            obj.save()

        # Deleting an Expense
        if "delete_expense" in request.POST:

            # Get the ID of the income first
            expenses_ID = request.POST.get("expense_ID")

            # Fetch the object related to the passed ID and delete it
            obj = get_object_or_404(expenses, id = expenses_ID)
            obj.delete()
        

        # For drawing charts
        year_input = request.POST.get('year', '').strip()

        if not year_input.isdigit():
            error = "Please select a valid year"
        else:
            selected_yr = int(year_input)

            if selected_yr < 2020 or selected_yr > current_yr:
                error = f"The year selected must be between 2020 and {current_yr}"
            else:
                # Query to group expenses and income by month for the selected year
                monthlyExpenses = (
                    expenses.objects.filter(ExpensesDate__year = selected_yr)
                    .annotate(month = TruncMonth('ExpensesDate'))
                    .values('month')
                    .annotate(total = Sum('ExpensesAmount'))
                    .order_by('month')
                )

                monthlyIncome = (
                    income.objects.filter(IncomeDate__year = selected_yr)
                    .annotate(month = TruncMonth('IncomeDate'))
                    .values('month')
                    .annotate(total = Sum('IncomeAmount'))
                    .order_by('month')
                )

                if monthlyExpenses.exists():
                    # Map month number to total
                    expenses_by_month = {
                        entry['month'].month: float(entry['total'])
                        for entry in monthlyExpenses
                    }

                    # Fill all 12 months, 0 for months with no data
                    expensesChart_labels = month_names
                    expensesChart_data = [expenses_by_month.get(m, 0) for m in range(1, 13)]

                if monthlyIncome.exists():
                    # Map month number to total
                    income_by_month = {
                        entry['month'].month: float(entry['total'])
                        for entry in monthlyIncome
                    }

                    # Fill all 12 months, 0 for months with no data
                    incomeChart_labels = month_names
                    incomeChart_data = [income_by_month.get(m, 0) for m in range(1, 13)]


    # Get total for all expenses, income and balance for the selected year
    totalExp = expenses.objects.filter(ExpensesDate__year = selected_yr).aggregate(total_amount = Sum('ExpensesAmount'))['total_amount'] or 0
    totalInc = income.objects.filter(IncomeDate__year = selected_yr).aggregate(total_amount = Sum('IncomeAmount'))['total_amount'] or 0
    totalBalance = totalInc - totalExp

    
    context = {
        'currentBalance': totalBalance,
        'totalIncome': totalInc,
        'totalExpenses': totalExp,

        # json.dumps() converts Python lists to JSON for chart.js to read
        'expenses_labels': json.dumps(expensesChart_labels),
        'income_labels': json.dumps(incomeChart_labels),
        'expenses_data': json.dumps(expensesChart_data),
        'income_data': json.dumps(incomeChart_data),
        'availableYears_Income': availableIncomeYears,
        'availableYears_Expenses': availableExpensesYears,
        'selected_yr': selected_yr,
        'error': error
    }

    return render(request, 'calc.html', context)

