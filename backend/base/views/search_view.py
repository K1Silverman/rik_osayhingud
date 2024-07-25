from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from ..models.dummyfie import DummyFie
from ..serializers import FieSerializer

class SearchFieView(APIView):
	def get(self, request):
		queryset = DummyFie.objects.all()
		query_string = request.query_params.get('queryString')
		if query_string:
			queryset = queryset.filter(Q(name__icontains=query_string) | Q(registry_code__icontains=query_string))
			serializer = FieSerializer(queryset, many=True)
			return Response(serializer.data)
		return Response([])

