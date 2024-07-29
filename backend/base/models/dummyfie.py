from django.db import models

## Dummy klass FIE otsingu jaoks, kuna ma ei olnud kindel kuidas soovitakse isikute
## otsingu jaoks FIEde ja füüsiliste isikute andmeid source'ida. Tõenäoliselt ideaalis
## tehaks seda Äriregistri API kaudu, kuid hetkel ei olnud kahjuks aega, et API ligipääsu taotleda.
## Genereerisin 25 FIEt avalikust andmestikust selle modeliga seotud tabelisse, et saaks demonstreerida
## Searchbari funktsionaalsust.
class DummyFie(models.Model):
	name = models.CharField(max_length=100)
	registry_code = models.CharField(max_length=7)