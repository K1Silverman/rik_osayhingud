from rest_framework import serializers
from ..models import Shareholder, Fie, Physical
from .fie_serializer import FieSerializer
from .physical_serializer	import PhysicalSerializer

class ShareholderSerializer(serializers.Serializer):
    class Meta:
        model = Shareholder
        fields = ['id', 'capacity', 'founder']

    def to_representation(self, instance):
        if instance.is_fie():
            return FieSerializer(instance).data
        elif instance.is_physical():
            return PhysicalSerializer(instance).data
        return super().to_representation(instance)