from django.urls import path
from . import views

app_name = 'rfq'

urlpatterns = [
	path('', views.index, name='index'),
	path('offer', views.offer, name='offer'),
	path('success', views.success, name='success')
]