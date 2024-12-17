from django.db import models
from django.conf import settings

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    description = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Salario base mensual
    max_budget_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Límite de gasto mensual 
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total de los gastos
    month = models.DateField()  # Mes de este presupuesto

    def add_expense(self, expense_amount):
        self.total_expenses += expense_amount
        if self.total_expenses > self.max_budget_amount:
            raise ValueError("El gasto excede el monto máximo del presupuesto.")
        self.save()

    def calculate_budget_percentage(self):
        return (self.total_expenses / self.salary) * 100 if self.salary else 0

    def calculate_savings_percentage(self):
        total_savings = sum(goal.saved_amount for goal in self.saving_goals.all())
        return (total_savings / self.salary) * 100 if self.salary else 0

    def calculate_extra_income_percentage(self):
        total_extra_income = sum(income.amount for income in self.extra_incomes.all())
        return (total_extra_income / self.salary) * 100 if self.salary else 0

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Presupuesto para {self.description} - {self.month} (Salario: Q.{self.salary}, Límite de Gasto: Q.{self.max_budget_amount}, Gastos Totales: Q.{self.total_expenses})"

class SavingGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saving_goals')
    description = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Objetivo de ahorro
    months_to_save = models.PositiveIntegerField()  # Número de meses para lograr el objetivo
    start_date = models.DateField()  # Fecha de inicio
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Ahorro acumulado
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Cantidad restante para alcanzar el objetivo

    @property
    def monthly_saving(self):
        return self.target_amount / self.months_to_save  # Cuánto ahorrar por mes

    def add_saving(self, amount):
        if self.saved_amount + amount > self.target_amount:
            raise ValueError("El monto ahorrado excede la meta.")
        self.saved_amount += amount
        self.update_remaining_amount()
        self.save()

    def update_remaining_amount(self):
        self.remaining_amount = self.target_amount - self.saved_amount
        self.save()

    def calculate_savings_percentage(self):
        return (self.saved_amount / self.user.budgets.first().salary) * 100 if self.user.budgets.first().salary else 0

    def __str__(self):
        return f"Objetivo de Ahorro: {self.description} - Ahorros Acumulados: Q.{self.saved_amount} - Meta: Q.{self.target_amount} - Faltante: Q.{self.remaining_amount}"

class ExtraIncome(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='extra_incomes')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto del ingreso extra
    date_received = models.DateField()  # Fecha de recepción

    def __str__(self):
        return f"Ingreso Extra: {self.description} - Monto: Q.{self.amount} - Fecha: {self.date_received}"

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=[
        ('F', 'Pago Fijo'),
        ('OE', 'Ocio y Entretenimiento'),
        ('OT', 'Otros'),
        ('AH', 'Ahorro')
    ])

    def __str__(self):
        return f"Gasto: {self.description} - {self.amount}"

    def save(self, *args, **kwargs):
        # Actualizar el total de gastos en el presupuesto correspondiente
        self.budget.total_expenses += self.amount
        self.budget.save()

        # Actualizar el objetivo de ahorro si el gasto es de tipo ahorro
        if self.category == 'savings':
            saving_goal = self.budget.saving_goals.first()
            if saving_goal:
                saving_goal.update_saving_goal(self.amount)

        super().save(*args, **kwargs)
