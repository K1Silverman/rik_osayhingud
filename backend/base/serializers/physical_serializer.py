
from ..models import Physical
# from .shareholder_serializer import ShareholderSerializer
from rest_framework import serializers

class PhysicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physical
        fields = ['id', 'capacity', 'founder', 'first_name', 'last_name', 'nic']