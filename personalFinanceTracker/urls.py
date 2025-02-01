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

urlpatterns = [
    # Endpoint to add an expense
    path('add-expense/', views.add_expense, name='add_expense'),

    # Endpoint to add income
    path('add-income/', views.add_income, name='add_income'),

    # Endpoint to fetch transaction history
    path('transaction-history/', views.transaction_history, name='transaction_history'),

    # Endpoint for expense list (specific to the logged-in user)
    path('expenses/', ExpenseListView.as_view(), name='expense-list'),
]
