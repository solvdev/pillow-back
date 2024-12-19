# Generated by Django 5.1.4 on 2024-12-16 00:43

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('total_income', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_expenses', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_savings', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('recurring', models.BooleanField(default=False)),
                ('recurring_cycle_end', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Fixed', 'Fixed'), ('Leisure', 'Leisure'), ('Debt Payment', 'Debt Payment'), ('Bill Payment', 'Bill Payment'), ('Other', 'Other')], max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='finances.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='finances.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavingGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('months_to_save', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('saved_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_goals', to='finances.budget')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_goals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]