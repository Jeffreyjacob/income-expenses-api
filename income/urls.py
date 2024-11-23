from django.urls import path
from income import views as api_views


urlpatterns = [
    path("",api_views.IncomeListAPIView.as_view(),name="income"),
    path("<int:id>",api_views.IncomeDetailAPIView.as_view(),name='income-detail')
]