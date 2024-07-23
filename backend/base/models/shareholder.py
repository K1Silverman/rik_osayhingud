from django.db import models

class Shareholder(models.Model):
	capacity = models.IntegerField()
	founder = models.BooleanField(default=True)

	def __str__(self):
		return self.name

class fie(Shareholder):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=7)

	def __str__(self):
		return self.name

class physical(Shareholder):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	nic = models.CharField(max_length=12)
	
	def __str__(self):
		return self.name