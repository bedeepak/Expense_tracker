from django.urls import path
from . import views

urlpatterns =[
    path('add/', views.add_expense, name='add_expense'),
]