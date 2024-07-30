from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import FieSerializer, PhysicalSerializer, EnterpriseSerializer, BaseShareholderSerializer
from ..models import Fie, Physical, Enterprise, Shareholder
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction


class EnterpriseView(APIView):
	def get(self, request, id=None):
		if id:
			enterprise = get_object_or_404(Enterprise, pk=id)
			serializer = EnterpriseSerializer(enterprise)
			return Response(serializer.data)
		else:
			return Response({"error": "Osaühingut ei leitud", 'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

	def post(self, request):
		enterprise_data = request.data
		shareholders_data = enterprise_data.pop('shareholder', [])
		if len(shareholders_data) == 0:
			return Response({"error": "Vigane vorm. Osaühingul peab olema vähemalt üks asutaja"}, status=status.HTTP_400_BAD_REQUEST)
		
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
			return Response(EnterpriseSerializer(updated_enterprise).data, status=status.HTTP_201_CREATED)
		return Response({'error': 'Vigane vorm', 'serializer_errors': enterprise_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
	
	def patch(self, request, id):
		data = request.data

		try:
			enterprise = Enterprise.objects.get(pk=id)
		except Enterprise.DoesNotExist:
			return Response({'error': 'Osaühingut ei leitud'}, status=status.HTTP_400_BAD_REQUEST)
		
		shareholders = data.get('shareholder', [])
		if len(shareholders) > 0:
			with transaction.atomic():
				current_shareholders = enterprise.shareholder.all()
				old_shareholders = [s for s in shareholders if 'id' in s]
				shareholders_to_remove = current_shareholders.difference(Shareholder.objects.filter(id__in=[s['id'] for s in old_shareholders]))
				enterprise.shareholder.remove(*shareholders_to_remove)
				for shareholder in shareholders:
					shareholder.pop('isEdit', None)
					shareholder_id = shareholder.get('id', None)
					if shareholder_id:
						shareholder_obj = get_object_or_404(Shareholder.objects.select_for_update(), pk=shareholder_id)
						if shareholder.get('nic', None):
							serializer = PhysicalSerializer(shareholder_obj, data=shareholder, partial=True)
							if serializer.is_valid(raise_exception=True):
								serializer.save()
							else:
								return Response({'error': 'Vigane vorm', 'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
						if shareholder.get('registry_code', None):
							serializer = FieSerializer(shareholder_obj, data=shareholder, partial=True)
							if serializer.is_valid(raise_exception=True):
								serializer.save()
							else:
								return Response({'error': 'Vigane vorm', 'serializer_errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
					else:
						if shareholder.get('nic', None):
							shareholder['founder'] = False
							shareholder_serializer = PhysicalSerializer(data=shareholder, partial=True)
							if shareholder_serializer.is_valid():
								new_shareholder = shareholder_serializer.save()
								enterprise.shareholder.add(new_shareholder)
							else: 
								return Response({'error': shareholder_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

						elif shareholder.get('registry_code', None):
							shareholder['founder'] = False
							shareholder_serializer = FieSerializer(data=shareholder, partial=True)
							if shareholder_serializer.is_valid():
								new_shareholder = shareholder_serializer.save()
								enterprise.shareholder.add(new_shareholder)

				enterprise.save()
			serializer = EnterpriseSerializer(enterprise, data=request.data, partial=True)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
		return Response({'error': 'Vigane vorm - puuduvad osanikud.'}, status=status.HTTP_400_BAD_REQUEST)