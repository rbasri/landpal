from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Quote 
from django.core.mail import send_mail
from landpal.settings import EMAIL_HOST_USER
import requests

# Create your views here.

def index(request):
	development = False
	try:
		if not development:
			address = request.POST['address']

			url1 = "https://realty-mole-property-api.p.rapidapi.com/properties"
			url2 = "https://realty-mole-property-api.p.rapidapi.com/rentalPrice"

			querystring1 = {"address": address}

			headers = {
			    'x-rapidapi-host': "realty-mole-property-api.p.rapidapi.com",
			    'x-rapidapi-key': ""
			}

			response = requests.request("GET", url1, headers=headers, params=querystring1)

			# Get first query results for sake of rent API query
			information = response.json()[0]
			address = information.get('formattedAddress')
			bedrooms = str(information.get('bedrooms'))
			bathrooms = str(information.get('bathrooms'))
			squareFootage = str(information.get('squareFootage'))
			propertyType = information.get('propertyType')
			
			# Create quote object
			streetaddr = information.get('addressLine1')
			city = information.get('city')
			state = information.get('state')
			zipcode = information.get('zipCode')
			timestamp = timezone.now()

			quote = Quote(
				address = streetaddr,
				city = city,
				state = state,
				zipcode = zipcode,
				timestamp = timestamp)


			querystring2 = {"compCount":"7","address":address,"propertyType":propertyType, "bedrooms":bedrooms, "bathrooms":bathrooms, "squareFootage":squareFootage}

			response2 = requests.request("GET", url2, headers=headers, params=querystring2)
			rentmid = response2.json().get('rent')
			renthigh = response2.json().get('rentRangeHigh')
			rentquote = min(rentmid*1.25, renthigh)
			# rentquote = 3000

			quote.rentquote = rentquote

			quote.save()

			return render(request, 'rfq/emailfunnel.html', {
				'quote': quote,
			})

		else:
			streetaddr = '15 oyster bay drive'
			city = 'rumson'
			state = 'nj'
			zipcode = '07760'
			timestamp = timezone.now()

			quote = Quote(
				address = streetaddr,
				city = city,
				state = state,
				zipcode = zipcode,
				timestamp = timestamp)

			rentquote = 3000

			quote.rentquote = rentquote

			quote.save()

			return render(request, 'rfq/emailfunnel.html', {
				'quote': quote,
			})

	except ValueError:
		error_message = "Sorry, we couldn't find that address. Please use format: 1500 Main Street, Somewhere, CA 11111."
		return render(request, 'rfq/error.html', {'error' : error_message})

	except ConnectionError:
		error_message = "Sorry, something went wrong. Please try again."
		return render(request, 'rfq/error.html', {'error' : error_message})	

def offer(request):
	try:
		email = request.POST['emailaddr']
		quote_id = request.POST['quote_id']

	except KeyError:
		error_message = "Sorry, something went wrong. Please try again."
		return render(request, 'rfq/error.html', {'error' : error_message})

	quote = get_object_or_404(Quote, pk=quote_id)
	quote.email = email
	quote.save()

	return render(request, 'rfq/rfq.html', {
		'quote': quote,
	})

def success(request):
	try:
		quote_id = request.POST['quote_id']

	except KeyError:
		error_message = "Sorry, something went wrong in trying to schedule that quote. Please try again."
		return render(request, 'rfq/error.html', {'error' : error_message})

	quote = get_object_or_404(Quote, pk=quote_id)
	quote.accepted = True
	quote.save()

	send_mail('Accepted quote for ' + quote.address, ' ', EMAIL_HOST_USER, [EMAIL_HOST_USER])

	return render(request, 'rfq/success.html')
