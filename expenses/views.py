from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from expenses import serializers as api_serializers
from expenses import models as api_models
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserOwnerToEditExpenses

# Create your views here.


class ExpensesListApiView(ListCreateAPIView):
    serializer_class = api_serializers.ExpensesSerializer
    permission_classes = [IsAuthenticated]
    queryset = api_models.Expenses.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailApiView(RetrieveUpdateDestroyAPIView):
     
        serializer_class = api_serializers.ExpensesSerializer
        queryset = api_models.Expenses.objects.all()
        permission_classes = [IsAuthenticated,IsUserOwnerToEditExpenses]
        lookup_field = "id"
        
        def get_queryset(self):
             return self.queryset.filter(owner=self.request.user)