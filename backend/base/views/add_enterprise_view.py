from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import FieSerializer, PhysicalSerializer, ShareholderSerializer, EnterpriseSerializer
from ..models import Fie, Physical, Enterprise
from django.core.exceptions import ValidationError
from rest_framework import status

class AddEnterpriseView(APIView):
	# def post(self, request):
	# 	data = request.data
	# 	print(f"request: {request.data}")
	# 	serializer = EnterpriseSerializer(data=data, context={'request': request})
		
	# 	if serializer.is_valid():
	# 		try:
	# 			enterprise = serializer.save()

	# 			response_data = EnterpriseSerializer(enterprise, context={'request': request}).data

	# 			return Response(response_data)
	# 		except ValidationError as e:
	# 			return Response({'errors': e.message_dict}, status=status.HTTP_400_BAD_REQUEST)
	# 	else:
	# 		print(serializer.errors)
	# 	return Response()

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
								shareholder = Fie.objects.create(**shareholder_data)
						else:
								return Response({"error": "Invalid shareholder type"}, status=status.HTTP_400_BAD_REQUEST)
						enterprise.shareholder.add(shareholder)
				updated_enterprise = Enterprise.objects.get(id=enterprise.id)
				print(f"shareholders: {updated_enterprise.shareholder.all()}")
				return Response(EnterpriseSerializer(updated_enterprise).data, status=status.HTTP_201_CREATED)
		return Response(enterprise_serializer.errors, status=status.HTTP_400_BAD_REQUEST)