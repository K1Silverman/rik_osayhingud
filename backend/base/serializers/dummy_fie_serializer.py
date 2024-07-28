from rest_framework import serializers
from ..models import DummyFie

class DummyFieSerializer(serializers.ModelSerializer):
	class Meta:
		model = DummyFie
		fields = '__all__'