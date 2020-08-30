from django.shortcuts import render
from django.core.mail import send_mail
from landpal.settings import EMAIL_HOST_USER

# Create your views here.

def index(request):
	return render(request, 'contact/contact.html')

def sendContact(request):
	try:
		email = request.POST['email']
		comments = request.POST['comments']

	except KeyError:
		return render(request, 'contact/contact.html')

	else:
		send_mail('New Contact from ' + email, comments, EMAIL_HOST_USER, [EMAIL_HOST_USER])

		return render(request, 'contact/success.html')