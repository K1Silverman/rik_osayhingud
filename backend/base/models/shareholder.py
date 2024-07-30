from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator

class Shareholder(models.Model):
	capacity = models.IntegerField(validators=[MinValueValidator(1)])
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
	first_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
	last_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
	nic = models.CharField(max_length=12, validators=[MinLengthValidator(7)])
	
	def __str__(self):
		return self.name