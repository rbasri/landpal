from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'homepage/homepage.html')

def site_map(request):
	return render(request, 'homepage/sitemap.xml', content_type='text/xml')
