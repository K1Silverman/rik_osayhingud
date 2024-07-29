from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import FieSerializer, PhysicalSerializer, ShareholderSerializer, EnterpriseSerializer, BaseShareholderSerializer
from ..models import Fie, Physical, Enterprise, Shareholder
from django.core.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction

class EnterpriseView(APIView):
	def get(self, request, id=None):

		if id:
			enterprise = Enterprise.objects.get(pk=id)
			serializer = EnterpriseSerializer(enterprise)
			return Response(serializer.data)
		else:
			return Response({"error": "Invalid enterprise id"}, status=status.HTTP_400_BAD_REQUEST)
		

	def post(self, request):
		enterprise_data = request.data
		print(f"request: {request.data}")
		shareholders_data = enterprise_data.pop('shareholder', [])
		
		enterprise_serializer = EnterpriseSerializer(data=enterprise_data)
		if enterprise_serializer.is_valid():
				enterprise = enterprise_serializer.save()
				
				for shareholder_data in shareholders_data:
						shareholder_type = shareholder_data.pop('shareholderType', None)
						if shareholder_type == 'physical':
								shareholder = Physical.objects.create(**shareholder_data)
						elif shareholder_type == 'fie':
								shareholder_data.pop('isEdit', None)
								shareholder = Fie.objects.create(**shareholder_data)
						else:
								return Response({"error": "Invalid shareholder type"}, status=status.HTTP_400_BAD_REQUEST)
						enterprise.shareholder.add(shareholder)
				updated_enterprise = Enterprise.objects.get(id=enterprise.id)
				print(f"shareholders: {updated_enterprise.shareholder.all()}")
				return Response(EnterpriseSerializer(updated_enterprise).data, status=status.HTTP_201_CREATED)
		return Response(enterprise_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def patch(self, request, id):
		data = request.data
		try:
			enterprise = Enterprise.objects.get(pk=id)
		except Enterprise.DoesNotExist:
			return Response({'error': 'Invalid enterprise id'}, status=status.HTTP_400_BAD_REQUEST)
		
		shareholders = data.get('shareholder', [])
		with transaction.atomic():
			if len(shareholders) > 0:
				enterprise.shareholder.clear()
				print(f"shareholders: {shareholders}")
				for shareholder in shareholders:
					
					shareholder_id = shareholder.get('id', None)
					print(f"id: {shareholder_id}")
					if shareholder_id:
						shareholder_obj = get_object_or_404(Shareholder.objects.select_for_update(), pk=shareholder_id)
						print(f"shareholder_obj: {shareholder_obj}")
						serializer = BaseShareholderSerializer(shareholder_obj, data=shareholder, partial=True)
						if serializer.is_valid():
							print(f"serializer.data: {serializer.data}")
							updated_shareholder = serializer.update(shareholder_obj, serializer.validated_data)
							enterprise.shareholder.add(updated_shareholder)
						else:
							return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
					else:
						if shareholder.get('nic', None):
							shareholder['founder'] = False
							shareholder_serializer = PhysicalSerializer(data=shareholder)
							if shareholder_serializer.is_valid():
								new_shareholder = shareholder_serializer.save()
								enterprise.shareholder.add(new_shareholder)			
											
						elif shareholder.get('registry_code', None):
							shareholder['founder'] = False
							shareholder_serializer = FieSerializer(data=shareholder)
							if shareholder_serializer.is_valid():
								new_shareholder = shareholder_serializer.save()
								enterprise.shareholder.add(new_shareholder)
				enterprise.save()

			serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)