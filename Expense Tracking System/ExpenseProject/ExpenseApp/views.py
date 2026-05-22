
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import * # Importing ALL the models
from django.db.models import Sum, Count, Avg, Max, Min # For calculating the total values needed


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
            return redirect('index')
        else:
            messages.info(request, 'INVALID details!!')
            return redirect('login')
    else:
        return render(request, 'login.html')


def calculating(request):

    if request.method == 'POST':
        # Adding Income
        if "add_income" in request.POST:
            # Get fields for Income
            incomeCategory = request.POST.get('Income_category')
            incomeAmount = request.POST.get('Income_amount')
            incomeDescription = request.POST.get('Income_description')
            incomeDate = request.POST.get('Income_date')

            # Adding income to the database
            incomeDetails = income.objects.create(
                IncomeCategory = incomeCategory,
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
            newIncomeCategory = request.POST.get("new_IncomeCategory")
            newIncomeAmount = request.POST.get("new_IncomeAmount")
            newIncomeDescription = request.POST.get("new_IncomeDescription")
            newIncomeDate = request.POST.get("new_IncomeDate")

            # Fetch the object related to the passed ID
            obj = get_object_or_404(income, id = income_ID)

            # Saving edited Income info
            obj.IncomeCategory = newIncomeCategory
            obj.IncomeAmount = newIncomeAmount
            obj.IncomeDescription = newIncomeDescription
            obj.IncomeDate = newIncomeDate
            obj.save()

        # Adding Expenses
        if "add_expense" in request.POST:
            # Get fields for Expenses
            expensesCategory = request.POST.get('Expenses_category')
            expensesAmount = request.POST.get('Expenses_amount')
            expensesDescription = request.POST.get('Expenses_description')
            expensesDate = request.POST.get('Expenses_date')

            # Adding expenses to the database
            expensesDetails = expenses.objects.create(
                ExpensesCategory = expensesCategory,
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
            newExpenseCategory = request.POST.get("new_ExpenseCategory")
            newExpenseAmount = request.POST.get("new_ExpenseAmount")
            newExpenseDescription = request.POST.get("new_ExpenseDescription")
            newExpenseDate = request.POST.get("new_ExpenseDate")

            # Fetch the object related to the passed ID
            obj = get_object_or_404(expenses, id = expenses_ID)

            # Saving edited Income info
            obj.ExpensesCategory = newExpenseCategory
            obj.ExpensesAmount = newExpenseAmount
            obj.ExpensesDescription = newExpenseDescription
            obj.ExpensesDate = newExpenseDate
            obj.save()

        # Get total for all expenses & income with their respective dates
        totalExp = expenses.objects.aggregate(total_amount = Sum('ExpensesAmount'))
        totalInc = income.objects.aggregate(total_amount = Sum('IncomeAmount'))
        latestExpDate = request.POST.get('latestExpDate') # Get the latest date for expenses
        latestIncDate = request.POST.get('latestIncDate') # Get the latest date for Income

        # Adding totals to the database
        TotalsDetails = totals.objects.create(
            TotalIncome = totalInc,
            TotalExpenses = totalExp,
            LatestTotalInc_As_of = latestIncDate,
            LatestTotalExp_As_of = latestExpDate
        )
        TotalsDetails.save()

        # For displaying a chart
        labels = []
        data = []

        querySet = income.objects.order_by('-IncomeAmount')
        for eachIncome in querySet:
            labels.append(eachIncome.IncomeDate)
            data.append(eachIncome.IncomeAmount)

    return render(request, 'calc.html', {
        'labels':labels,
        'data':data
    })

