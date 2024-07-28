from django.urls import path
from . import views

urlpatterns = [
	path('search', views.SearchFieView.as_view(), name='search'),
	path('add', views.AddEnterpriseView.as_view(), name='add_enterprise'),
]