from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    """
    A form for creating and updating Expense instances.

    This form is based on the Expense model and includes fields for
    description, amount, category, date, and notes. It uses Django's
    ModelForm to automatically generate form fields based on the model's
    attributes.

    The form also includes custom validation to ensure that the amount is
    a positive value.
    """

    class Meta:
        model = Expense
        fields = ['description', 'amount', 'category', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_amount(self):
        """
        Validates that the amount entered is a positive number.

        Raises:
            ValidationError: If the amount is not greater than zero.
        """
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be a positive number.")
        return amount