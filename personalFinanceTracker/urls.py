# from django.urls import path
# from . import views
# from .views import ExpenseListView

# urlpatterns = [
#     path('add-expense/', views.add_expense, name='add_expense'),
#     path('add-income/', views.add_income, name='add_income'),
#     path('transaction-history/', views.transaction_history, name='transaction_history'),
#     path('expenses/', ExpenseListView.as_view(), name='expense-list')
# ]


from django.urls import path
from . import views
from .views import ExpenseListView
from .views import weekly_report, monthly_report, seasonal_report

urlpatterns = [
    # Endpoint to add an expense
    path('add-expense/', views.add_expense, name='add_expense'),

    # Endpoint to add income
    path('add-income/', views.add_income, name='add_income'),

    # Endpoint to fetch transaction history
    path('transaction-history/', views.transaction_history, name='transaction_history'),

    # Endpoint for expense list (specific to the logged-in user)
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),

    path('weekly-report/', weekly_report, name='weekly-report'),

    path('monthly-report/', monthly_report, name='monthly-report'),

    path('seasonal-report/', seasonal_report, name='seasonal-report'),
]
