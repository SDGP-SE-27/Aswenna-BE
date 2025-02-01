from rest_framework import serializers
from .models import Expense  # Import your model
from .models import Income

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id','date ', 'expense_type', 'amount', 'description', 'created_at']  # Include all fields you need

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id','date ', 'income_type', 'amount', 'description', 'created_at'] 
