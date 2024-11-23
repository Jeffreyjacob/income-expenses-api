from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from income import models as api_models
from income import serializers as api_serializers 
from .permissions import IsUserOwnerToEditIncome
from rest_framework.permissions import IsAuthenticated

# Create your views here


class IncomeListAPIView(ListCreateAPIView):
    
    serializer_class = api_serializers.IncomeSerializer
    queryset = api_models.Income.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = api_serializers.IncomeSerializer
    permission_classes = [IsAuthenticated,IsUserOwnerToEditIncome]
    queryset = api_models.Income.objects.all()
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
