from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from ..models import DummyFie, Enterprise
from ..serializers import DummyFieSerializer, EnterpriseSerializer

class SearchFieView(APIView):
	def get(self, request):
		search_mode = request.query_params.get('searchMode')
		if search_mode == 'fie':
			query_string = request.query_params.get('queryString')
			if query_string:
				queryset = DummyFie.objects.all()
				
				queryset = queryset.filter(Q(name__icontains=query_string) | Q(registry_code__icontains=query_string)).distinct()
				serializer = DummyFieSerializer(queryset, many=True)
				return Response(serializer.data)
		
		if search_mode == 'enterprise':
			query_string = request.query_params.get('queryString')
			if query_string:
				queryset = Enterprise.objects.all()
				queryset = queryset.filter(Q(name__icontains=query_string) |
															Q(registry_code__icontains=query_string) |
															Q(shareholder__fie__name__icontains=query_string) |
															Q(shareholder__fie__registry_code__icontains=query_string) |
															Q(shareholder__physical__first_name__icontains=query_string) |
															Q(shareholder__physical__last_name__icontains=query_string) |
															Q(shareholder__physical__nic__icontains=query_string)).distinct()
				
				serializer = EnterpriseSerializer(queryset, many=True)
				return Response(serializer.data)

		return Response([])

