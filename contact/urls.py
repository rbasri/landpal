from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
	path('', views.index, name='index'),
	path('sent', views.sendContact, name="send_contact"),
]