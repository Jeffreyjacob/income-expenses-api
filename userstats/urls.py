from django.urls import path
from userstats import views as api_views



urlpatterns = [
    path("expense_category_data",api_views.ExpenseSummaryStats.as_view()),
    path("income_source_data",api_views.IncomeSourceSummaryStats.as_view())
]