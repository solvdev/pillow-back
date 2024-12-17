from django.contrib import admin
from .models import Budget, ExtraIncome, SavingGoal, Expense

# Registra los modelos en el admin
admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(ExtraIncome)
admin.site.register(SavingGoal)

