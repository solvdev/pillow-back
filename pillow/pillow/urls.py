from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, include
from django.http import HttpResponseRedirect
from rest_framework.routers import DefaultRouter
from finances.views import (
    BudgetViewSet,
    ExtraIncomeViewSet,
    ExpenseViewSet,
    SavingGoalViewSet,
)
from accounts.views import *

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename="budget")
router.register(r"incomes", ExtraIncomeViewSet, basename="income")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"saving-goals", SavingGoalViewSet, basename="saving-goal")
router.register(r"users", UsersModelViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponseRedirect("/admin/")),  # Redirección a /admin
    path("api/v1/", include(router.urls)),  # Prefijo api/v1 para las rutas
    path("api/v1/signin", signin, name='signin'),  # Nueva ruta para el inicio de sesión
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
