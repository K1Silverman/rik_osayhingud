from ..models import Fie
from rest_framework import serializers


class FieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fie
        fields = ['id', 'capacity', 'founder', 'name', 'registry_code']
