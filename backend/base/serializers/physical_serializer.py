from ..models import Physical
from rest_framework import serializers

class PhysicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physical
        fields = '__all__'