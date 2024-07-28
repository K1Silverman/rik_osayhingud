from .shareholder_serializer import ShareholderSerializer
from .fie_serializer import FieSerializer
from .physical_serializer import PhysicalSerializer
from ..models import Shareholder

class BaseShareholderSerializer(ShareholderSerializer):
    class Meta(ShareholderSerializer.Meta):
        model = Shareholder
        fields = ShareholderSerializer.Meta.fields

    def to_representation(self, instance):
        data = super(ShareholderSerializer, self).to_representation(instance)

        if instance.is_fie():
            fie_serializer = FieSerializer(instance.fie)
            data.update(fie_serializer.data)
        elif instance.is_physical():
            physical_serializer = PhysicalSerializer(instance.physical)
            data.update(physical_serializer.data)

        return data