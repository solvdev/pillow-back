from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Budget, ExtraIncome, SavingGoal, Expense
from .serializers import BudgetSerializer, ExtraIncomeSerializer, SavingGoalSerializer, ExpenseSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Budget.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        budget_instance = self.get_object()
        if not budget_instance:
            return Response({"error": "Budget object not found."}, status=status.HTTP_404_NOT_FOUND)
        
        old_budget = Budget.objects.get(pk=budget_instance.pk)
        updated_data = serializer.validated_data

        for field in ['salary', 'total_expenses', 'total_savings']:
            if field in updated_data:
                old_value = getattr(old_budget, field)
                new_value = updated_data[field]
                amount_change = new_value - old_value
                self.update_budget_totals(budget_instance, amount_change, **{f'{field}_change': True})

        serializer.save()

    def perform_destroy(self, instance):
        old_budget = Budget.objects.get(pk=instance.pk)
        self.update_budget_totals(old_budget, -old_budget.total_income, income=True)
        self.update_budget_totals(old_budget, -old_budget.total_expenses, expense=True)
        self.update_budget_totals(old_budget, -old_budget.total_savings, saving_goal=True)
        instance.delete()

class ExtraIncomeViewSet(viewsets.ModelViewSet):
    serializer_class = ExtraIncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ExtraIncome.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        income_instance = self.get_object()
        if not income_instance:
            return Response({"error": "Income object not found."}, status=status.HTTP_404_NOT_FOUND)

        old_amount = income_instance.amount
        new_amount = serializer.validated_data['amount']
        income_instance.budget.total_income -= old_amount
        income_instance.budget.total_income += new_amount
        income_instance.budget.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        expense_instance = self.get_object()
        if not expense_instance:
            return Response({"error": "Expense object not found."}, status=status.HTTP_404_NOT_FOUND)

        old_amount = expense_instance.amount
        new_amount = serializer.validated_data['amount']
        expense_instance.budget.total_expenses -= old_amount
        expense_instance.budget.total_expenses += new_amount
        expense_instance.budget.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class SavingGoalViewSet(viewsets.ModelViewSet):
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SavingGoal.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        goal_instance = self.get_object()
        if not goal_instance:
            return Response({"error": "SavingGoal object not found."}, status=status.HTTP_404_NOT_FOUND)

        old_goal_amount = goal_instance.goal_amount
        new_goal_amount = serializer.validated_data['goal_amount']
        goal_instance.budget.total_saving_goals -= old_goal_amount
        goal_instance.budget.total_saving_goals += new_goal_amount
        goal_instance.budget.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
