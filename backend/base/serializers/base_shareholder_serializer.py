from .shareholder_serializer import ShareholderSerializer
from .fie_serializer import FieSerializer
from .physical_serializer import PhysicalSerializer
from ..models import Shareholder, Fie, Physical

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
    
    def create(self, validated_data):
        print(f"val_data: {str(validated_data)}")
        if 'registry_code' in validated_data:
            
            fie_obj = Fie.objects.create(**validated_data)
            print(f"fie_obj: {fie_obj}")
            return fie_obj
        if 'nic' in validated_data:
            physical_obj = Physical.objects.create(**validated_data)
            print(f"physical_obj: {physical_obj}")
            return physical_obj

    def update(self, instance, validated_data):
        """
        Updates a Shareholder instance with validated data.
        """
        # Update the instance fields using validated_data
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance