from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    """
    Represents a financial expense entry for a user.

    Attributes:
        user (ForeignKey): The user who owns this expense record.
        description (CharField): A short description of the expense.
        amount (DecimalField): The monetary value of the expense.
        category (CharField): The category under which the expense falls (e.g., Food, Travel).
        date (DateField): The date when the expense occurred.
        notes (TextField): Optional additional details about the expense.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user associated with this expense."
    )
    description = models.CharField(
        max_length=200,
        help_text="Brief description of the expense."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Expense amount in currency format."
    )
    category = models.CharField(
        max_length=100,
        help_text="Category of the expense (e.g., Food, Travel, Utilities)."
    )
    date = models.DateField(
        help_text="Date when the expense was incurred."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Optional notes or comments about the expense."
    )

    def __str__(self):
        """
        Returns a human-readable string representation of the expense.
        Useful in Django admin and shell.
        """
        return f"{self.description} - {self.amount}"
