from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from .shareholder import Shareholder

class Enterprise(models.Model):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=7)
	proprietor_first_entry_date = models.DateField(validators=[MinValueValidator(timezone.now().date())])
	total_capital = models.IntegerField(validators=[MinValueValidator(2500)])
	fie = models.BooleanField(default=False)
	shareholder = models.ManyToManyField(Shareholder)
