from rest_framework import serializers
from ..models import DummyFie

class FieSerializer(serializers.ModelSerializer):
	class Meta:
		model = DummyFie
		fields = '__all__'