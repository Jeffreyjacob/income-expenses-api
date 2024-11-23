from rest_framework import serializers
from expenses import models as api_models

class ExpensesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Expenses
        fields = [
            'date',
            'id',
            'description',
            'amount',
            'category'
        ]