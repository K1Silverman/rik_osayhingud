from rest_framework import serializers
from ..models import Enterprise
from .base_shareholder_serializer import BaseShareholderSerializer
	
class EnterpriseSerializer(serializers.ModelSerializer):
	shareholder = BaseShareholderSerializer(many=True, read_only=True)
	class Meta:
		model = Enterprise
		fields = '__all__'