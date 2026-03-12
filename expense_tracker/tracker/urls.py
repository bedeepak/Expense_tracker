from django.urls import path
from .views import export_expenses_csv
from . import views

urlpatterns =[
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_expense, name='add_expense'),
    path('export-csv/', export_expenses_csv, name='export_csv'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:id>/',views.edit_expense, name ='edit_expense'),
    path('delete/<int:id>/',views.delete_expense,name='delete_expense'),
]