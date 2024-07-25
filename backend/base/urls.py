from django.urls import path
from . import views

urlpatterns = [
	path('fie', views.SearchFieView.as_view(), name='fie_search'),
]