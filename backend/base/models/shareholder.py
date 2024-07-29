from django.db import models

class Shareholder(models.Model):
	capacity = models.IntegerField()
	founder = models.BooleanField(default=True)

	def is_fie(self):
		return getattr(self, 'fie', None) is not None
	
	def is_physical(self):
		return getattr(self, 'physical', None) is not None


## Fie peaks tegelikult olema eraldi ForeingKey relationina kuid ei soovinud DummyFie modelit
## kasutada, kuna tolle modeli eesmärk oli puhtalt andmete hoiustamine Searchbari tarbeks.
class Fie(Shareholder):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=10)

	def __str__(self):
		return self.name
	
class Physical(Shareholder):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	nic = models.CharField(max_length=12)
	
	def __str__(self):
		return self.name