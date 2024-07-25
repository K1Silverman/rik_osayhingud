from django.db import models

class DummyFie(models.Model):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=7)