from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate
from .models import Expense
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

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
    context = {
        'expenses': expenses
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