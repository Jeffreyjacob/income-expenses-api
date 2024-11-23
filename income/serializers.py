from rest_framework import serializers
from income import models as api_models

class IncomeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Income
        fields = [
            'date',
            'id',
            'description',
            'amount',
            'source'
        ]