from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

import json
import csv
import pickle

from .models import Expense
from .forms import ExpenseForm

# Load ML model for expense category prediction
model = pickle.load(open('tracker/expense_model.pkl', 'rb'))

def predict_category_ml(text):
    """Predict category using ML model."""
    try:
        return model.predict([text])[0]
    except Exception:
        return "Other"  # fallback category if model fails

@login_required
def add_expense(request):
    """Add a new expense."""
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.category = predict_category_ml(expense.description)
            expense.save()
            return redirect('add_expense')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})

def signup(request):
    """User registration."""
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
    """Display user's dashboard with expenses and analytics."""
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    # Monthly totals
    monthly_data = (
        Expense.objects
        .filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )
    months = [item['month'].strftime('%B %Y') for item in monthly_data]
    monthly_totals = [float(item['total']) for item in monthly_data]

    # Category totals
    category_data = (
        Expense.objects
        .filter(user=request.user)
        .values('category')
        .annotate(total=Sum('amount'))
    )
    labels = [item['category'] for item in category_data]
    data = [float(item['total']) for item in category_data]

    # Total per category
    category_totals = {}
    for cat in ['Food','Transport','Entertainment','Utilities','Groceries','Health','Education','Shopping']:
        category_totals[f"{cat.lower()}_total"] = Expense.objects.filter(user=request.user, category=cat).aggregate(total=Sum('amount'))['total'] or 0

    expense_count = Expense.objects.filter(user=request.user).count()

    context = {
        'expenses': expenses,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
        'months': json.dumps(months),
        'monthly_totals': json.dumps(monthly_totals),
        'total_expenses': Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0,
        'expense_count': expense_count,
        **category_totals
    }

    return render(request, 'tracker/dashboard.html', context)

@login_required
def edit_expense(request, id):
    """Edit an existing expense."""
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
    """Delete an expense."""
    expense = get_object_or_404(Expense, id=id, user=request.user)
    if request.method == "POST":
        expense.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})

@login_required
def export_expenses_csv(request):
    """Export user's expenses as CSV."""
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Category', 'Date', 'Notes'])

    for expense in expenses:
        writer.writerow([expense.description, expense.amount, expense.category, expense.date, expense.notes])

    return response