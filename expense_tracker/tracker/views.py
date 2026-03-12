from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Sum

import json
import csv

# Create your views here.

from .forms import ExpenseForm

@login_required
def add_expense(request):
    """
    View function to handle the addition of a new expense.

    This view processes both GET and POST requests. For GET requests, it
    renders an empty ExpenseForm for the user to fill out. For POST
    requests, it validates the submitted form data and saves a new
    Expense instance if the data is valid. If the form is invalid, it
    re-renders the form with error messages.

    Args:
        request: The HTTP request object.
    Returns:
        An HTTP response with the rendered form or a redirect after successful submission.
    """
    if request.method == "POST":
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.category = predict_category(expense.description)
            expense.save()
            return redirect('add_expense')
    else:
        form = ExpenseForm()
        
    return render(request, 'tracker/add_expense.html', {'form': form})

def signup(request):
    """
    View function to handle user registration.

    This view processes both GET and POST requests. For GET requests, it
    renders an empty UserCreationForm for the user to fill out. For POST
    requests, it validates the submitted form data and creates a new
    user if the data is valid. If the form is invalid, it re-renders the
    form with error messages.

    Args:
        request: The HTTP request object.
    Returns:
        An HTTP response with the rendered form or a redirect after successful registration.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add_expense')
    else:
        form = UserCreationForm()
    
    return render(request, 'tracker/signup.html', {'form': form})

@login_required
def dashboard(request):
    """
    View function to display the user's dashboard.

    This view retrieves all expenses associated with the currently logged-in
    user and renders them in the dashboard template.

    Args:
        request: The HTTP request object.
    Returns:
        An HTTP response with the rendered dashboard containing the user's expenses.
    """
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    category_data = (
        Expense.objects
        .filter(user=request.user)
        .values('category')
        .annotate(total=Sum('amount'))
    )
    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    total_expenses = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
    food_total = Expense.objects.filter(user=request.user, category='Food').aggregate(total=Sum('amount'))['total'] or 0
    transport_total = Expense.objects.filter(user=request.user, category='Transport').aggregate(total=Sum('amount'))['total'] or 0
    entertainment_total = Expense.objects.filter(user=request.user, category='Entertainment').aggregate(total=Sum('amount'))['total'] or 0
    utilities_total = Expense.objects.filter(user=request.user, category='Utilities').aggregate(total=Sum('amount'))['total'] or 0
    groceries_total = Expense.objects.filter(user=request.user, category='Groceries').aggregate(total=Sum('amount'))['total'] or 0
    health_total = Expense.objects.filter(user=request.user, category='Health').aggregate(total=Sum('amount'))['total'] or 0
    education_total = Expense.objects.filter(user=request.user, category='Education').aggregate(total=Sum('amount'))['total'] or 0
    shopping_total = Expense.objects.filter(user=request.user, category='Shopping').aggregate(total=Sum('amount'))['total'] or 0
    expense_count = Expense.objects.filter(user=request.user).count()
    context = {
        'expenses': expenses,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'total_expenses': total_expenses,
        'food_total': food_total,
        'transport_total': transport_total,
        'entertainment_total': entertainment_total,
        'utilities_total': utilities_total,
        'groceries_total': groceries_total,
        'health_total': health_total,
        'education_total': education_total,
        'shopping_total': shopping_total,
        'expense_count': expense_count
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def edit_expense(request, id):
    """
    View function to handle editing an existing expense.

    This view processes both GET and POST requests. For GET requests, it
    retrieves the specified Expense instance and renders a pre-filled
    ExpenseForm for the user to edit. For POST requests, it validates the
    submitted form data and updates the Expense instance if the data is
    valid. If the form is invalid, it re-renders the form with error
    messages.

    Args:
        request: The HTTP request object.
        expense_id: The ID of the expense to be edited.
    Returns:
        An HTTP response with the rendered form or a redirect after successful update.
    """
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'tracker/edit_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    """
    View function to handle the deletion of an expense.

    This view retrieves the specified Expense instance and deletes it from
    the database. After deletion, it redirects the user back to the
    dashboard.

    Args:
        request: The HTTP request object.
        expense_id: The ID of the expense to be deleted.
    Returns:
        An HTTP response that redirects to the dashboard after deletion.
    """
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect('dashboard')
    
    return render(request, 'tracker/delete_expense.html', {'expense': expense})

def predict_category(description):
    """
    Placeholder function for predicting the category of an expense based on its description.

    This function is intended to be implemented in the future to analyze the
    description of an expense and predict its category using machine learning
    or rule-based logic.

    Args:
        description: A string containing the description of the expense.
    Returns:
        A string representing the predicted category of the expense.
    """
    description = description.lower()

    keywords = {
        "Food": ["restaurant", "cafe", "dining", "meal", "food"],
        "Transport": ["taxi", "bus", "train", "transport", "uber", "lyft"],
        "Entertainment": ["movie", "concert", "entertainment", "game", "show"],
        "Utilities": ["electricity", "water", "gas", "utility", "internet"],
        "Groceries": ["grocery", "supermarket", "groceries", "food store"],
        "Health": ["pharmacy", "doctor", "health", "medicine", "hospital"],
        "Education": ["book", "course", "education", "school", "university"],
        "Shopping": ["clothing", "electronics", "shopping", "mall", "store"],
        "Other": []
    }

    for category, words in keywords.items():
        for word in words:
            if word in description:
                return category
            
    return "Other"

@login_required
def export_expenses_csv(request):
    """
    View function to export the user's expenses as a CSV file.

    This view retrieves all expenses associated with the currently logged-in
    user and generates a CSV file containing the expense data. The CSV file
    is then returned as an HTTP response for the user to download.

    Args:
        request: The HTTP request object.
    Returns:
        An HTTP response with the generated CSV file for download.
    """
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Category', 'Date', 'Notes'])

    for expense in expenses:
        writer.writerow([expense.description, expense.amount, expense.category, expense.date, expense.notes])

    return response