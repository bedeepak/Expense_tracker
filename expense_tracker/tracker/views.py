from django.shortcuts import render, redirect

# Create your views here.

from .forms import ExpenseForm

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