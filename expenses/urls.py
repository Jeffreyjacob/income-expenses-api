from django.urls import path
from expenses import views as api_views


urlpatterns = [
    path("",api_views.ExpensesListApiView.as_view(),name="expenses"),
    path("<int:id>/",api_views.ExpenseDetailApiView.as_view(),name="expense-detail")
]