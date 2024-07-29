from django.urls import path
from . import views

urlpatterns = [
	path('search', views.SearchFieView.as_view(), name='search'),
	path('enterprise', views.EnterpriseView.as_view(), name='add_enterprise'),
	path('enterprise/<int:id>', views.EnterpriseView.as_view(), name='get_enterprise'),
]