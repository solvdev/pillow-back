from rest_framework import serializers
from .models import Budget, SavingGoal, ExtraIncome, Expense

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class ExtraIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraIncome
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingGoal
        fields = '__all__'
