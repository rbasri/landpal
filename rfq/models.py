from django.db import models

# Create your models here.

from django.utils import timezone

import datetime

class Quote(models.Model):
	address = models.CharField(max_length=200, default='')
	city = models.CharField(max_length=50, default='')
	state = models.CharField(max_length=20, default='')
	zipcode = models.CharField(max_length=10, default='')
	timestamp = models.DateTimeField()
	email = models.CharField(max_length=50, default='')
	rentquote = models.IntegerField(default=0)
	accepted = models.BooleanField(default=False)

	def __str__(self):
		return self.email + ' | ' + str(self.timestamp)