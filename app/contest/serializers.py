from core.models import Contest
from rest_framework import serializers

class ContestSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contest
        fields = '__all__'
