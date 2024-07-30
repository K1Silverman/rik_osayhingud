from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.utils import timezone
from .shareholder import Shareholder

class Enterprise(models.Model):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=7, unique=True, validators=[MinLengthValidator(7)])
	first_entry_date = models.DateField(validators=[MaxValueValidator(timezone.now().date())], default=timezone.now)
	total_capital = models.IntegerField(validators=[MinValueValidator(2500)])
	shareholder = models.ManyToManyField(Shareholder)