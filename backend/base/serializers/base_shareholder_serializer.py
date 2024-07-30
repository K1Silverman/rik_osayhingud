from .shareholder_serializer import ShareholderSerializer
from .fie_serializer import FieSerializer
from .physical_serializer import PhysicalSerializer
from ..models import Shareholder, Fie, Physical

class BaseShareholderSerializer(ShareholderSerializer):
    class Meta(ShareholderSerializer.Meta):
        model = Shareholder
        fields = '__all__'

    def to_representation(self, instance):
        data = super(ShareholderSerializer, self).to_representation(instance)
        if instance.is_fie():
            fie_serializer = FieSerializer(instance.fie)
            data.update(fie_serializer.data)
        elif instance.is_physical():
            physical_serializer = PhysicalSerializer(instance.physical)
            data.update(physical_serializer.data)

        return data
    
    def create(self, validated_data):
        if 'registry_code' in validated_data:
            fie_obj = Fie.objects.create(**validated_data)
            return fie_obj
        if 'nic' in validated_data:
            physical_obj = Physical.objects.create(**validated_data)
            return physical_obj

    def update(self, instance, validated_data):
        for field in self.Meta.model._meta.get_fields():
            if field.name in validated_data:
                setattr(instance, field.name, validated_data[field.name])
        instance.save()
        return instance